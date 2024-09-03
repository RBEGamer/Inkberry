import io
import csv
from matplotlib import pyplot as plt


from DisplayFramework import BaseTile, TileSpecification, ResourceHelper, DeviceSpecification
from DisplayFramework.pysvg import structure, builders, text
from DisplayFramework.tiles import ImageTile
from PIL import Image


class TableViewTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": BaseTile.TileParameterTypes.STRING,
            "figure_aspect_ratio": BaseTile.TileParameterTypes.STRING,
            "scale_factor": BaseTile.TileParameterTypes.FLOAT,
            "tile_size": BaseTile.TileParameterTypes.INTEGER,
            "title": BaseTile.TileParameterTypes.STRING,
            "figure_scale_factor": BaseTile.TileParameterTypes.FLOAT,
            "image_rotation": BaseTile.TileParameterTypes.INTEGER,
            "show_lines": BaseTile.TileParameterTypes.BOOL
        }, "default": {
            "url": "",
            "figure_aspect_ratio": "7:3",
            "scale_factor": 1.0,
            "tile_size": 8,
            "title": "",
            "figure_scale_factor": 1.0,
            "image_rotation": 0,
            "show_lines": False
        }
    }

    data_columns: [str] = []
    data_rows: [str] = []


    def __init__(self, _hardware: DeviceSpecification.DeviceSpecification, _specification: TileSpecification.TileSpecification):
        super().__init__(_hardware, _specification)

    def update(self) -> bool:
        # FETCH RESOURCE
        url: str = self.get_spec_parameters('url')
        table_path: str = ResourceHelper.ResourceHelper.FetchContent(url, self.spec.name)

        if not table_path.endswith(".csv"):
            pass
        try:
            with open(table_path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0

                self.data_columns = []
                self.data_rows = []

                for row in csv_reader:
                    if line_count <= 0:
                        self.data_columns = row
                    else:
                        self.data_rows.append(row)
                    line_count = line_count + 1
                return True
        except Exception as e:
            print(e)
            return False


    def generate_table_figure(self, _data_columns: [], _data_rows: [[str]]):

        apr_w: float = 7.0
        apr_h: float = 3.0

        figure_aspect_ratio: str = self.get_spec_parameters('figure_aspect_ratio')
        figure_scale_factor: float = self.get_spec_parameters('figure_scale_factor')
        title: str = self.get_spec_parameters('title')
        tile_size: int = self.get_spec_parameters('tile_size')
        show_lines: bool = self.get_spec_parameters('show_lines')

        if ":" in figure_aspect_ratio:
            spr: [str] = figure_aspect_ratio.split(":")
            apr_w = max(1.0, float(spr[0]))
            apr_h = max(1.0, float(spr[1]))


        # CREATE TABLE VIEW IN MATPLOTLIB
        plt.rcParams["figure.figsize"] = [apr_w * figure_scale_factor, apr_h * figure_scale_factor]
        plt.rcParams["figure.autolayout"] = True

        fig = plt.figure(figsize=(apr_w * figure_scale_factor, apr_h * figure_scale_factor), dpi=300)
        ax = plt.subplot()

        if len(title) > 0:
            ax.set_title(title, fontsize=tile_size)

        rows = _data_rows[::-1]
        ncols: int = len(_data_columns)
        nrows: int = len(_data_rows)
        # TODO GENERATE TABLE FIGURE
        ax.set_xlim(0, ncols)
        ax.set_ylim(0, nrows )

        # Add table's main text
        for i in range(nrows):
            for j, column in enumerate(_data_columns):
                if j == 0:
                    ha = 'left'
                else:
                    ha = 'center'

                text_label = str(rows[i][j])
                weight = 'normal'

                ax.annotate(
                    xy=(j + .2, i + .5),
                    text=text_label,
                    ha=ha,
                    va='center',
                    weight=weight
                )

        # Add column names
        for index, c in enumerate(_data_columns):
            if index == 0:
                ha = 'left'
            else:
                ha = 'center'
            ax.annotate(
                xy=(index + .2, nrows + .25),
                text=_data_columns[index],
                ha=ha,
                va='bottom',
                weight='bold'
            )

        # Add dividing lines
        if show_lines:
            ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=1.5, color='black', marker='', zorder=4)
            ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color='black', marker='', zorder=4)

            for x in range(1, nrows):
                ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color='gray', ls=':', zorder=3, marker='')


        ax.set_axis_off()
        ax.axis('tight')
        ax.axis('off')

        fig.tight_layout()
        plt.interactive(False)

        return plt


    def render(self) -> structure.Svg:

        scale_factor: float = self.get_spec_parameters('scale_factor')

        plot_figure = self.generate_table_figure(self.data_columns, self.data_rows)

        # GENERATE IMAGE FROM PLOT
        plot_image = io.BytesIO()
        plot_figure.savefig(plot_image, format='png', transparent=True, dpi=300)
        plt.close()
        plot_image.seek(0)

        # CREATE PIL IMAGE TO GENERATE SVG ELEMENT
        loaded_image = Image.open(plot_image)
        return ImageTile.ImageTile.generate_image_container(loaded_image, self.spec, _scale_factor=scale_factor, _preserve_aspect_ratio=True)
