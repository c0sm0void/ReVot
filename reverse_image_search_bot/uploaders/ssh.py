import os
import logging
from tempfile import NamedTemporaryFile
from getpass import getpass
import paramiko
from contextlib import contextmanager
from .base_uploader import UploaderBase

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SSHUploader(UploaderBase):
    """Upload files to an ssh server via paramiko http://www.paramiko.org/

    Attributes:
        configuration (:obj:`dict`): Configuration of this uploader
        ssh (:obj:`paramiko.client.SSHClient`): Connection to the ssh server
        sftp (:obj:`paramiko.sftp_client.SFTPClient`): Connection via sftp to the ssh server
    Args:
        configuration (:obj:`dict`): Configuration of this uploader. Must contain these keys: host, user, password,
            key_filename, upload_dir, ssh_authentication
        connect (:obj:`bool`): If the uploader should directly connect to the server
    """

    _mandatory_configuration = {'host': str, 'user': str, 'password': str, 'upload_dir': str}

    def __init__(self, configuration: dict, connect: bool = False):
        self.ssh = None
        self.sftp = None

        # Get password securely from environment or input prompt
        self.configuration = configuration
        self.configuration['password'] = os.getenv("SSH_PASSWORD") or getpass("Enter SSH password: ")

        super().__init__(configuration, connect)

    @contextmanager
    def ssh_connection(self):
        """Context manager to handle SSH connection lifecycle."""
        self.connect()
        try:
            yield
        finally:
            self.close()

    def connect(self):
        """Establish SSH and SFTP connection."""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.configuration.get('key_filename', None):
                self.ssh.connect(self.configuration['host'],
                                 username=self.configuration['user'],
                                 password=self.configuration['password'],
                                 key_filename=self.configuration['key_filename'])
            else:
                self.ssh.connect(self.configuration['host'],
                                 username=self.configuration['user'],
                                 password=self.configuration['password'])
            self.sftp = self.ssh.open_sftp()
            logger.info(f"SSH connection established to {self.configuration['host']}")
        except paramiko.SSHException as e:
            raise ConnectionError(f"SSH connection failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during connection: {str(e)}")

    def close(self):
        """Close SSH and SFTP connections."""
        if self.sftp:
            self.sftp.close()
            logger.info("SFTP connection closed")
        if self.ssh:
            self.ssh.close()
            logger.info("SSH connection closed")

    def upload(self, file, filename: str = None, upload_dir: str = None):
        """Upload file to the ssh server

        Args:
            file: Path to file on file system or a file like object
            filename (:obj:`str`): Filename on the server. This is mandatory if your file is a file-like object.
            upload_dir (:obj:`str`): Upload directory on server. Joins with the configurations upload_dir
        """
        logger.info(f"Starting upload for file: {filename}")

        # Check if file is a file-like object
        is_file_object = bool(getattr(file, 'read', False))
        if is_file_object:
            if filename is None:
                raise ValueError('filename must be set when file is a file-like object')
            with NamedTemporaryFile(delete=False) as new_file:
                file.seek(0)
                new_file.write(file.read())
                real_file = new_file.name
        else:
            real_file = file
            filename = filename or os.path.basename(real_file)

        # Determine upload directory
        upload_dir = os.path.join(self.configuration['upload_dir'], upload_dir) if upload_dir else self.configuration['upload_dir']
        upload_path = os.path.join(upload_dir, filename)

        # Perform the upload
        with self.ssh_connection():
            self.sftp.put(real_file, upload_path)
            logger.info(f"File uploaded successfully to {upload_path}")

        # Cleanup temporary file if created
        if is_file_object:
            os.unlink(real_file)
            logger.info(f"Temporary file {real_file} deleted")
