import functools
from torch import nn

class UNetSkipConnectionLayer(nn.Module):
    def __init__(self, out_c, inner_c, outter=False, in_c=None, inner=False, use_drop=False,
                 norm_layer=nn.BatchNorm2d, submodule=False):
        super().__init__()
        self.outter = outter

        if in_c is None:
            in_c = out_c

        if type(norm_layer) == functools.partial:
            use_bias = (norm_layer.func == nn.InstanceNorm2d)
        else:
            use_bias = (norm_layer == nn.InstanceNorm2d)

        if self.outter:
            self.outconv = nn.Conv2d(2, out_c, kernel_size=1, stride=1)

        downrelu = nn.LeakyReLU(0.2, True)
        downConv = nn.Conv2d(in_c, inner_c, kernel_size=4, stride=2, padding=1, bias=use_bias)
        uprelu = nn.ReLU(True)
        upNorm = norm_layer(out_c)
        downNorm = norm_layer(inner_c)

        if inner:
            upConv = nn.ConvTranspose2d(inner_c, out_c, kernel_size=4, stride=2, padding=1, bias=use_bias)
            down = [downrelu, downConv]
            up = [uprelu, upConv, upNorm]
            layers = down + up
        elif outter:
            upConv = nn.ConvTranspose2d(inner_c * 2, out_c, kernel_size=4, stride=2, padding=1)
            down = [downConv]
            up = [uprelu, upConv]
            layers = down + [submodule] + up
        else:
            upConv = nn.ConvTranspose2d(inner_c * 2, out_c, kernel_size=4, stride=2, padding=1, bias=use_bias)
            down = [downrelu, downConv, downNorm]
            up = [uprelu, upConv, upNorm]
            if use_drop:
                layers = down + [submodule] + up + [nn.Dropout(0.5)]
            else:
                layers = down + [submodule] + up

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        if self.outter:
            return self.outconv(torch.cat([x, self.model(x)], dim=1))
        else:
            return torch.cat([x, self.model(x)], dim=1)


class UNetGenerator(nn.Module):
    def __init__(self, in_c, out_c, num_downs=8, ngf=64, norm_layer=nn.BatchNorm2d, use_drop=False):
        super().__init__()
        block = UNetSkipConnectionLayer(8 * ngf, 8 * ngf, inner=True, norm_layer=norm_layer)
        for i in range(num_downs - 5):
            block = UNetSkipConnectionLayer(8 * ngf, 8 * ngf, norm_layer=norm_layer, use_drop=use_drop, submodule=block)
        block = UNetSkipConnectionLayer(4 * ngf, 8 * ngf, norm_layer=norm_layer, submodule=block)
        block = UNetSkipConnectionLayer(2 * ngf, 4 * ngf, norm_layer=norm_layer, submodule=block)
        block = UNetSkipConnectionLayer(ngf, 2 * ngf, norm_layer=norm_layer, submodule=block)
        self.model = UNetSkipConnectionLayer(out_c, ngf, in_c=in_c, norm_layer=norm_layer, submodule=block, outter=True)

    def forward(self, x):
        return self.model(x)