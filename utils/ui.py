import sys
import time
import numpy as np


class ProgressBar(object):
    """Progress indicator that works within jupyter-notebooks
       without the need of having JavaScript activated.
       
    References:
        Taken from: Keras
    """
    def __init__(self, max_value, width=32, interval=0.01):
        """Creates a progress indicator instance.
        Parameters
        ----------
        max_value: int
            The maximum progress value.
        width: int, optional
            The width of the progress bar.
        interval: float, optional
            The minimum visual progress update interval (in seconds)
        """
        self.width = width
        self.max_value = max_value
        self.sum_params = {}
        self.unique_params = []
        self.start = time.time()
        self.last_update = 0
        self.interval = interval
        self.total_width = 0
        self.seen_so_far = 0

    def update(self, value, params=[], force=False):
        """Updates the progress bar.
        Parameters
        ----------
        value: int
            The value of the progess.
        params: list(tuple(str, float)), optional
            List of parameters to show as a tuple of (name, value).
            The progress bar will display averages for these values.
        force: Boolean, optional
            Force visual progress update.
        """
        for k, v in params:
            if k not in self.sum_params:
                self.sum_params[k] = [v * (value - self.seen_so_far), value - self.seen_so_far]
                self.unique_params.append(k)
            else:
                self.sum_params[k][0] += v * (value - self.seen_so_far)
                self.sum_params[k][1] += (value - self.seen_so_far)
        self.seen_so_far = value

        now = time.time()

        if not force and (now - self.last_update) < self.interval:
            return

        prev_total_width = self.total_width
        sys.stdout.write("\b" * prev_total_width)
        sys.stdout.write("\r")

        numdigits = int(np.floor(np.log10(self.max_value))) + 1
        barstr = '%%%dd/%%%dd [' % (numdigits, numdigits)
        bar = barstr % (value, self.max_value)
        prog = float(value) / self.max_value
        prog_width = int(self.width * prog)
        if prog_width > 0:
            bar += ('=' * (prog_width-1))
            if value < self.max_value:
                bar += '>'
            else:
                bar += '='
        bar += ('.' * (self.width - prog_width))
        bar += ']'
        sys.stdout.write(bar)
        self.total_width = len(bar)

        if value:
            time_per_unit = (now - self.start) / value
        else:
            time_per_unit = 0
        eta = time_per_unit * (self.max_value - value)
        info = ''
        if value < self.max_value:
            info += ' - ETA: %ds' % eta
        else:
            info += ' - %ds' % (now - self.start)
        for k in self.unique_params:
            info += ' - %s:' % k
            if type(self.sum_params[k]) is list:
                avg = self.sum_params[k][0] / max(1, self.sum_params[k][1])
                if abs(avg) > 1e-3:
                    info += ' %.4f' % avg
                else:
                    info += ' %.4e' % avg
            else:
                info += ' %s' % self.sum_params[k]

        self.total_width += len(info)
        if prev_total_width > self.total_width:
            info += ((prev_total_width - self.total_width) * " ")

        sys.stdout.write(info)
        sys.stdout.flush()

        if value >= self.max_value:
            sys.stdout.write("\n")

        self.last_update = now