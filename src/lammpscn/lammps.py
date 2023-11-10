from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
    line_cell_magic,
)

from lammps import lammps


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
    def version(self, line=None):
        return self.lmp.version()

    @line_magic
    def get_thermo(self, line):
        return self.lmp.get_thermo(line)

    @line_magic
    def get_natoms(self, line=None):
        return self.lmp.get_natoms()

    @line_magic
    def last_thermo(self, line=None):
        return self.lmp.last_thermo()

    @line_magic
    def reset_box(self, line=None):
        return self.lmp.reset_box()

    @line_magic
    def extract_setting(self, line):
        """
        https://docs.lammps.org/Python_module.html#lammps.lammps.extract_setting
        """
        return self.lmp.extract_setting(line)

    @line_magic
    def extract_global(self, line=None):
        return self.lmp.extract_global()

    @line_magic
    def extract_box(self, line=None):
        """
        https://docs.lammps.org/Python_module.html#lammps.lammps.extract_box
        """
        return self.lmp.extract_box()

    @line_magic
    def extract_atom(self, line):
        """
        https://docs.lammps.org/Python_module.html#lammps.lammps.extract_atom
        """
        return self.lmp.extract_atom(line.split())

    @line_magic
    def create_atoms(self, line):
        """
        https://docs.lammps.org/Python_module.html#lammps.lammps.create_atoms
        """
        return self.lmp.create_atoms(line.split())

    @line_magic
    def close(self):
        return self.lmp.close()
    
    #TODO : how to register lammps.numpy wrapper?


def load_ipython_extension(ipython):
    magics = LammpsMagic(ipython)
    ipython.register_magics(magics)
