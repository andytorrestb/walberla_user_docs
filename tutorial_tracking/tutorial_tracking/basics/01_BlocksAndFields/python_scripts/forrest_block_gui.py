import re
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider, RadioButtons

def parse_block_data(log_data):
    pattern = re.compile(r"<(\d+),(\d+),(\d+)>[, ]+<(\d+),(\d+),(\d+)>")
    blocks = [((int(x0), int(y0), int(z0)), (int(x1), int(y1), int(z1)))
              for x0, y0, z0, x1, y1, z1 in pattern.findall(log_data)]
    data = []
    for idx, ((x0, y0, z0), (x1, y1, z1)) in enumerate(blocks):
        cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        data.append((idx, cx, cy, cz, dx, dy, dz))
    return pd.DataFrame(data, columns=["Index", "X", "Y", "Z", "DX", "DY", "DZ"])

def create_cube(xc, yc, zc, dx, dy, dz):
    x0, x1 = xc - dx/2, xc + dx/2
    y0, y1 = yc - dy/2, yc + dy/2
    z0, z1 = zc - dz/2, zc + dz/2
    corners = [
        [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]
    ]
    return [
        [corners[i] for i in [0, 1, 2, 3]],
        [corners[i] for i in [4, 5, 6, 7]],
        [corners[i] for i in [0, 1, 5, 4]],
        [corners[i] for i in [2, 3, 7, 6]],
        [corners[i] for i in [1, 2, 6, 5]],
        [corners[i] for i in [3, 0, 4, 7]],
    ]

def plot_interactive(df):
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Interactive Block Viewer')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    points = []
    blocks, labels = [], []
    for row in df.itertuples():
        faces = create_cube(row.X, row.Y, row.Z, row.DX, row.DY, row.DZ)
        cube = Poly3DCollection(faces, edgecolor='k', facecolor='skyblue', alpha=0.3)
        ax.add_collection3d(cube)
        point = ax.scatter(row.X, row.Y, row.Z, c='b', marker='o', visible=False)
        points.append(point)
        label = ax.text(row.X, row.Y, row.Z,
                        f'{int(row.Index)} ({int(row.X)},{int(row.Y)},{int(row.Z)})',
                        fontsize=7, color='red')
        blocks.append(cube)
        labels.append(label)

    ax_slider_az = plt.axes([0.3, 0.03, 0.45, 0.02])
    ax_slider_el = plt.axes([0.3, 0.00, 0.45, 0.02])
    slider_az = Slider(ax_slider_az, 'Azimuth', 0, 360, valinit=45)
    slider_el = Slider(ax_slider_el, 'Elevation', 0, 90, valinit=30)
    slider_az.on_changed(lambda val: update_view(ax, slider_el, slider_az))
    slider_el.on_changed(lambda val: update_view(ax, slider_el, slider_az))

    ax_mode = plt.axes([0.01, 0.02, 0.15, 0.08])
    mode_selector = RadioButtons(ax_mode, ['Blocks', 'Centroids'], active=0)

    def switch_mode(label):
        show_blocks = (label == 'Blocks')
        for block in blocks:
            block.set_visible(show_blocks)
        for point in points:
            point.set_visible(not show_blocks)
        fig.canvas.draw_idle()

    mode_selector.on_clicked(switch_mode)

    def update_view(ax, slider_el, slider_az):
        ax.view_init(elev=slider_el.val, azim=slider_az.val)
        ax.figure.canvas.draw_idle()

    plt.subplots_adjust(left=0.18, bottom=0.12)
    plt.show()

if __name__ == "__main__":
    log_data = """Global coordinates: [ <0,0,0>, <5,4,6> ]
Global coordinates: [ <5,0,0>, <10,4,6> ]
Global coordinates: [ <10,0,0>, <15,4,6> ]
Global coordinates: [ <0,4,0>, <5,8,6> ]
Global coordinates: [ <5,4,0>, <10,8,6> ]
Global coordinates: [ <10,4,0>, <15,8,6> ]
Global coordinates: [ <0,0,6>, <5,4,12> ]
Global coordinates: [ <5,0,6>, <10,4,12> ]
Global coordinates: [ <10,0,6>, <15,4,12> ]
Global coordinates: [ <0,4,6>, <5,8,12> ]
Global coordinates: [ <5,4,6>, <10,8,12> ]
Global coordinates: [ <10,4,6>, <15,8,12> ]
Global coordinates: [ <0,0,12>, <5,4,18> ]
Global coordinates: [ <5,0,12>, <10,4,18> ]
Global coordinates: [ <10,0,12>, <15,4,18> ]
Global coordinates: [ <0,4,12>, <5,8,18> ]
Global coordinates: [ <5,4,12>, <10,8,18> ]
Global coordinates: [ <10,4,12>, <15,8,18> ]
Global coordinates: [ <0,0,18>, <5,4,24> ]
Global coordinates: [ <5,0,18>, <10,4,24> ]
Global coordinates: [ <10,0,18>, <15,4,24> ]
Global coordinates: [ <0,4,18>, <5,8,24> ]
Global coordinates: [ <5,4,18>, <10,8,24> ]
Global coordinates: [ <10,4,18>, <15,8,24> ]
"""

    df = parse_block_data(log_data)
    plot_interactive(df)
