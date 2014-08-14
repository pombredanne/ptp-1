"""

:synopsis: Specialized Report class for the tool Nmap.

.. moduleauthor:: Tao Sauvage

"""

from libptp.report import AbstractReport
from libptp.tools.nmap.parser import NmapXMLParser


class NmapReport(AbstractReport):
    """Retrieve the information of a Nmap report."""

    __tool__ = 'nmap'
    __parsers__ = [NmapXMLParser]

    def __init__(self):
        """Initialize NmapReport."""
        AbstractReport.__init__(self)

    @classmethod
    def is_mine(cls, pathname, filename='*.xml'):
        """Check if it is a Nmap report and if it can handle it.

        :param str pathname: Path to the report directory.
        :param str filename: Regex matching the report file.

        :return: `True` if it supports the report, `False` otherwise.
        :rtype: :class:`bool`

        """
        return AbstractReport.is_mine(
            cls.__parsers__,
            pathname=pathname,
            filename=filename)

    def parse(self, pathname=None, filename='*.xml'):
        """Parse a Nmap report.

        :param str pathname: Path to the report directory.
        :param str filename: Regex matching the report file.

        :return: List of dicts where each one represents a discovery from the
            report.
        :rtype: :class:`list`

        """
        # Reconstruct the path to the report if any.
        self.fullpath = self._recursive_find(pathname, filename)
        if not self.fullpath:
            return []
        self.fullpath = self.fullpath[0]
        # Find the corresponding parser.
        self._init_parser(self.fullpath)
        # Parse specific stuff.
        self.metadata = self.parser.parse_metadata()
        self.vulns = self.parser.parse_report()
        return self.vulns
