import io
import csv
from matplotlib import pyplot as plt


from DisplayFramework import BaseTile, TileSpecification, ResourceHelper
from DisplayFramework.pysvg import structure, builders, text
from DisplayFramework.tiles import ImageTile
from PIL import Image


class TableViewTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": "str",
            "figure_aspect_ratio":"str",
            "scale_factor":"float",
            "tile_size": "int",
            "title": "str",
            "figure_scale_factor": "float",
            "image_rotation": "int"
        },"default":{
            "url": "",
            "figure_aspect_ratio": "7:3",
            "scale_factor": 1.0,
            "tile_size": 8,
            "title": "",
            "figure_scale_factor": 1.0,
            "image_rotation": 0
        }
    }

    data_columns: [str] = []
    data_rows: [str] = []



    def update_parameters(self, _parameter: dict):
        for k, v in _parameter.items():
            pass

    def update(self):
        # FETCH RESOURCE
        table_path: str = ResourceHelper.ResourceHelper.FetchContent(self.spec.parameters.get('url', ''), self.spec.name)

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
        except Exception as e:
            print(e)


    def generate_table_figure(self, _data_columns: [], _data_rows: [[str]]):

        apr_w: float = 7.0
        apr_h: float = 3.0
        if ":" in self.spec.parameters.get('figure_aspect_ratio', "7:3"):
            spr: [str] = self.spec.parameters.get('figure_aspect_ratio', "7:3").split(":")
            apr_w = max(1.0, float(spr[0]))
            apr_h = max(1.0, float(spr[1]))


        # CREATE TABLE VIEW IN MATPLOTLIB
        figure_scale_factor: float = abs(float(self.spec.parameters.get('figure_scale_factor', 1.0)))
        plt.rcParams["figure.figsize"] = [apr_w * figure_scale_factor, apr_h * figure_scale_factor]
        plt.rcParams["figure.autolayout"] = True

        fig = plt.figure(figsize=(apr_w * figure_scale_factor, apr_h * figure_scale_factor), dpi=300)
        ax = plt.subplot()

        ax.set_title(self.spec.parameters.get('title', ''), fontsize=int(self.spec.parameters.get('tile_size', 8)))

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
        if bool(int(self.spec.parameters.get('show_lines', 0))):
            ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=1.5, color='black', marker='', zorder=4)
            ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color='black', marker='', zorder=4)
            for x in range(1, nrows):
                ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color='gray', ls=':', zorder=3, marker='')



        # ABTRACT FROM IMAGE
        # IMAGE GENERATION FUNCTION


        ax.set_axis_off()
        ax.axis('tight')
        ax.axis('off')

        fig.tight_layout()
        plt.interactive(False)

        return plt

    def get_parameter_types(self) -> dict:
        return self.DEFAULT_PARAMETER['types']

    def get_parameter_defaults(self) -> dict:
        return self.DEFAULT_PARAMETER['default']

    def get_parameter_current(self) -> dict:
        return self.spec.parameters



    def render(self) -> structure.Svg:

        plot_figure = self.generate_table_figure(self.data_columns, self.data_rows)

        # GENERATE IMAGE FROM PLOT
        plot_image = io.BytesIO()
        plot_figure.savefig(plot_image, format='png', transparent=True, dpi=300)
        plot_image.seek(0)

        # CREATE PIL IMAGE TO GENERATE SVG ELEMENT
        loaded_image = Image.open(plot_image)
        return ImageTile.ImageTile.generate_image_container(loaded_image, self.spec)
