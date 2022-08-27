"""
A progressbar capable of having a label inside
"""
from tkinter import ttk


class LabeledProgressBar(ttk.Progressbar):  # pylint: disable=too-many-ancestors
    """A progress bar that can have a label inside"""

    _inst_count = 0  # Number of class instances created.

    def __init__(self, *args, **kwargs):
        classname = type(self).__name__
        assert (
            "style" not in kwargs
        ), f'{classname} initializer does not support providing a ttk "style".'
        type(self)._inst_count += 1  # Increment class attribute.
        # Create a style with a different name for each instance.

        self.style = ttk.Style()
        self.stylename = f"text.Horizontal.TProgressbar{self._inst_count}"
        self.style.layout(
            self.stylename,
            [
                (
                    "Horizontal.Progressbar.trough",
                    {
                        "children": [
                            (
                                "Horizontal.Progressbar.pbar",
                                {"side": "left", "sticky": "ns"},
                            )
                        ],
                        "sticky": "nsew",
                    },
                ),
                ("Horizontal.Progressbar.label", {"sticky": ""}),
            ],
        )

        self.style.configure(self.stylename, text="0.00%")
        kwargs.update(style=self.stylename)
        super().__init__(*args, **kwargs)

    def set_label(self, string):
        """sets the label of the progress bar"""
        self.style.configure(self.stylename, text=string)

    def auto_set_label_perc(self, auto_color=True):
        """sets the label to match its progress percent"""
        progress, maximum = self["value"], self["maximum"]
        perc_string = f"{progress/float(maximum)*100:.2f}%"
        self.style.configure(self.stylename, text=perc_string)
        if auto_color:
            self.set_auto_color()

    def set_auto_color(self):
        """sets the background of the progress bar"""
        if self["value"] < self["maximum"]:
            self.set_color("yellow", "yellow")
        else:
            self.set_color("green", "green")

    def set_color(self, foreground, background):
        """sets the color of the progressbar"""
        return  # todo


if __name__ == "__main__":
    pass
