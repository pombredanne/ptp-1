"""

:synopsis: Specialized Parser classes for W3AF.

.. moduleauthor:: Tao Sauvage

"""

import re

from lxml.etree import LxmlError

from libptp import constants
from libptp.exceptions import NotSupportedVersionError
from libptp.parser import XMLParser


class W3AFXMLParser(XMLParser):
    """W3AF XML specialized parser."""

    __tool__ = 'w3af'
    __format__ = 'xml'
    __version__ = ['1.6.0.2', '1.6.0.3']

    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    INFO = 'Information'

    RANKING_SCALE = {
        HIGH: constants.HIGH,
        MEDIUM: constants.MEDIUM,
        LOW: constants.LOW,
        INFO: constants.INFO}

    def __init__(self, fullpath):
        """Initialize W3AFXMLParser.

        :param str fullpath: full path to the report file.

        """
        XMLParser.__init__(self, fullpath)
        self.re_version = re.compile(r'Version: (\S*)\s')

    @classmethod
    def is_mine(cls, fullpath):
        """Check if it is a supported W3AF report.

        :param str fullpath: full path to the report file.

        :return: `True` if it supports the report, `False` otherwise.
        :rtype: :class:`bool`

        """
        try:
            stream = cls.handle_file(fullpath)
        except (ValueError, LxmlError):
            return False
        if stream.find('.//w3af-version') is None:
            return False
        return True

    def parse_metadata(self):
        """Parse the metadata of the report.

        :raises: :class:`NotSupportedVersionError` -- if it does not support
            the version of this report.

        :return: The metadata of the report.
        :rtype: dict

        """
        raw_metadata = self.stream.find('.//w3af-version').text
        # Find the version of w3af.
        version = self.re_version.findall(raw_metadata)
        if len(version) >= 1:  # In case we found several version numbers.
            version = version[0]
        # Reconstruct the metadata
        # TODO: Retrieve the other metadata likes the date, etc.
        metadata = {'version': version,}
        if self.check_version(metadata):
            self.metadata = metadata
        else:
            raise NotSupportedVersionError(
                'PTP does NOT support this version of W3AF.')

    def parse_report(self):
        """Parse the results of the report.

        :return: List of dicts where each one represents a discovery.
        :rtype: :class:`list`

        """
        self.vulns = [
            {'ranking': self.RANKING_SCALE[vuln.get('severity')],}
            for vuln in self.stream.findall('.//vulnerability')]
        return self.vulns
