import numpy as np

bigFont = 8
smallFont = 7


def colorHtml(r, g, b):
    return '#%02x%02x%02x' % (int(r), int(g), int(b))


def colormap(color, colorGrad=0.5):
    if color == 'specialblack':
        return '#dfdfdf', '000000'
    colorGrad = 0.9 if color == 'window' else colorGrad

    color = namedColors[color]
    color = np.array([int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)])
    return colorHtml(*color), colorHtml(*(color * colorGrad))


namedColors = {'aliceblue': '#F0F8FF',
               'antiquewhite': '#FAEBD7',
               'aqua': '#00FFFF',
               'aquamarine': '#7FFFD4',
               'azure': '#F0FFFF',
               'beige': '#F5F5DC',
               'bisque': '#FFE4C4',
               'black': '#000000',
               'blanchedalmond': '#FFEBCD',
               'blue': '#0000FF',
               'blueviolet': '#8A2BE2',
               'brown': '#A52A2A',
               'burlywood': '#DEB887',
               'cadetblue': '#5F9EA0',
               'chartreuse': '#7FFF00',
               'chocolate': '#D2691E',
               'coral': '#FF7F50',
               'cornflowerblue': '#6495ED',
               'cornsilk': '#FFF8DC',
               'crimson': '#DC143C',
               'cyan': '#00FFFF',
               'darkblue': '#00008B',
               'darkcyan': '#008B8B',
               'darkgoldenrod': '#B8860B',
               'darkgray': '#A9A9A9',
               'darkgreen': '#006400',
               'darkgrey': '#A9A9A9',
               'darkkhaki': '#BDB76B',
               'darkmagenta': '#8B008B',
               'darkolivegreen': '#556B2F',
               'darkorange': '#FF8C00',
               'darkorchid': '#9932CC',
               'darkred': '#8B0000',
               'darksalmon': '#E9967A',
               'darkseagreen': '#8FBC8F',
               'darkslateblue': '#483D8B',
               'darkslategray': '#2F4F4F',
               'darkslategrey': '#2F4F4F',
               'darkturquoise': '#00CED1',
               'darkviolet': '#9400D3',
               'deeppink': '#FF1493',
               'deepskyblue': '#00BFFF',
               'dimgray': '#696969',
               'dimgrey': '#696969',
               'dodgerblue': '#1E90FF',
               'firebrick': '#B22222',
               'floralwhite': '#FFFAF0',
               'forestgreen': '#228B22',
               'fuchsia': '#FF00FF',
               'gainsboro': '#DCDCDC',
               'ghostwhite': '#F8F8FF',
               'gold': '#FFD700',
               'goldenrod': '#DAA520',
               'gray': '#808080',
               'green': '#43ea2e',
               'greenyellow': '#ADFF2F',
               'grey': '#808080',
               'honeydew': '#F0FFF0',
               'hotpink': '#FF69B4',
               'indianred': '#CD5C5C',
               'indigo': '#4B0082',
               'ivory': '#FFFFF0',
               'khaki': '#F0E68C',
               'lavender': '#E6E6FA',
               'lavenderblush': '#FFF0F5',
               'lawngreen': '#7CFC00',
               'lemonchiffon': '#FFFACD',
               'lightblue': '#ADD8E6',
               'lightcoral': '#F08080',
               'lightcyan': '#E0FFFF',
               'lightgoldenrodyellow': '#FAFAD2',
               'lightgray': '#D3D3D3',
               'lightgreen': '#90EE90',
               'lightgrey': '#D3D3D3',
               'lightpink': '#FFB6C1',
               'lightsalmon': '#FFA07A',
               'lightseagreen': '#20B2AA',
               'lightskyblue': '#87CEFA',
               'lightslategray': '#778899',
               'lightslategrey': '#778899',
               'lightsteelblue': '#B0C4DE',
               'lightyellow': '#FFFFE0',
               'lime': '#00FF00',
               'limegreen': '#32CD32',
               'linen': '#FAF0E6',
               'magenta': '#FF00FF',
               'maroon': '#800000',
               'mediumaquamarine': '#66CDAA',
               'mediumblue': '#0000CD',
               'mediumorchid': '#BA55D3',
               'mediumpurple': '#9370DB',
               'mediumseagreen': '#3CB371',
               'mediumslateblue': '#7B68EE',
               'mediumspringgreen': '#00FA9A',
               'mediumturquoise': '#48D1CC',
               'mediumvioletred': '#C71585',
               'midnightblue': '#191970',
               'mintcream': '#F5FFFA',
               'mistyrose': '#FFE4E1',
               'moccasin': '#FFE4B5',
               'navajowhite': '#FFDEAD',
               'navy': '#000080',
               'oldlace': '#FDF5E6',
               'olive': '#808000',
               'olivedrab': '#6B8E23',
               'orange': '#ffab50',
               'orangered': '#FF4500',
               'orchid': '#DA70D6',
               'palegoldenrod': '#EEE8AA',
               'palegreen': '#98FB98',
               'paleturquoise': '#AFEEEE',
               'palevioletred': '#DB7093',
               'papayawhip': '#FFEFD5',
               'peachpuff': '#FFDAB9',
               'peru': '#CD853F',
               'pink': '#FFC0CB',
               'plum': '#d59aff',
               'powderblue': '#B0E0E6',
               'purple': '#800080',
               'rebeccapurple': '#663399',
               'red': '#FF0000',
               'rosybrown': '#BC8F8F',
               'royalblue': '#4169E1',
               'saddlebrown': '#8B4513',
               'salmon': '#FA8072',
               'sandybrown': '#F4A460',
               'seagreen': '#2E8B57',
               'seashell': '#FFF5EE',
               'sienna': '#A0522D',
               'silver': '#C0C0C0',
               'slateblue': '#6A5ACD',
               'slategray': '#708090',
               'slategrey': '#708090',
               'snow': '#FFFAFA',
               'springgreen': '#00FF7F',
               'steelblue': '#4682B4',
               'tan': '#D2B48C',
               'teal': '#008080',
               'thistle': '#D8BFD8',
               'tomato': '#FF6347',
               'turquoise': '#40E0D0',
               'violet': '#EE82EE',
               'wheat': '#F5DEB3',
               'white': '#FFFFFF',
               'whitesmoke': '#F5F5F5',
               'yellow': '#fff400',
               'yellowgreen': '#9ACD32',
               'alf2': '#a1e9e9',
               'skyblue': '#6c8ed6',
               'skyblue2': '#87CEEB',
               'window': '#fcf9f6'}

state2color = {"default": ('window', 'black'),
               "online": ('green', 'white'),
               "idle": ('green', 'white'),
               "on": ('green', 'white'),
               "ok": ('green', 'white'),
               "off": ('alf2', 'white'),
               "open": ('green', 'white'),
               "close": ('alf2', 'white'),
               "closed": ('alf2', 'white'),
               "operation": ('green', 'white'),
               "simulation": ('plum', 'white'),

               "wiping": ('skyblue', 'white'),
               "integrating": ('skyblue', 'white'),
               "reading": ('skyblue', 'white'),
               "exposing": ('skyblue', 'white'),
               "loading": ('skyblue', 'white'),
               "initialising": ('skyblue', 'white'),
               "warming": ('skyblue', 'white'),
               "moving": ('skyblue', 'white'),
               "opening": ('skyblue', 'white'),
               "closing": ('skyblue', 'white'),
               "turning_off": ('skyblue', 'white'),
               "switching": ('skyblue', 'white'),
               "busy": ('skyblue', 'white'),
               "openred": ('skyblue', 'white'),
               "openblue": ('skyblue', 'white'),
               "nan": ('orange', 'white'),
               "undef": ('orange', 'white'),
               "unknown": ('orange', 'white'),
               "invalid": ('orange', 'white'),
               "blocked": ('orange', 'white'),
               "midstate": ('orange', 'white'),
               "loaded": ('orange', 'white'),
               "safestop": ('orange', 'white'),
               "offline": ('specialblack', 'white'),
               "abort": ('red', 'white'),
               "failed": ('red', 'white'),
               "error": ('red', 'white'),
               "alarm": ('red', 'white'),
               "alert": ('red', 'white'),
               "regular": ('white', 'black'),
               "success": ('chartreuse', 'white'),
               "warning": ('orange', 'white'),
               "orangered": ('orangered', 'white'),
               "monitoring": ('skyblue', 'white'),
               "undefined": ('red', 'white'),
               }


def colorWidget(key):
    return state2color[key.lower()]
