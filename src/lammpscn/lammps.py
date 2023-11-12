from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
    line_cell_magic,
)

from lammps import lammps, IPyLammps, PyLammps


@magics_class
class LammpsMagic(Magics):
    def __init__(self, shell):
        super(LammpsMagic, self).__init__(shell)
        self.lmp = lammps()

    @line_cell_magic
    def cmd(self, line, cell=None):
        """
        register a magic command for IPython.

        Example:
            One command:
                %cmd print "hello world"
            Multiple commands:
                %%cmd
                print "hello chemist"
                print "hello physicist"

        Args:
            line (str): just string
            cell (str, optional): commands seperated by \n. Defaults to None if one command.

        Returns:
            str: echo formatted string
        """
        if cell:
            self.lmp.commands_string(cell)
            return cell
        else:
            self.lmp.command(line)
            return line

    @line_magic
    def lmp(self, line=None):
        return self.lmp

    @line_magic
    def pylmp(self, line=None):
        return PyLammps(ptr=self.lmp)

    @line_magic
    def ipylmp(self, line=None):
        return IPyLammps(ptr=self.lmp)

    @line_magic
    def close(self):
        return self.lmp.close()


def load_ipython_extension(ipython):
    magics = LammpsMagic(ipython)
    ipython.register_magics(magics)
