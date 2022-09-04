"""
Automatic zmq service to send/receive based on whether we are first service or not.
"""
import json
import multiprocessing
import threading
from queue import Empty
import zmq
from discord_vid.task import Task

# from discord_vid.config import get_config
class ZMQService:
    """
    ZMQ service. It creates a server + client.
    If a server already exists, that's fine.
    The client is then used to send the actual request to wherever the server is.
    """

    def __init__(self):
        self.port = 22635

        self.task_queue = multiprocessing.Queue()
        try:
            self.server = ZMQServer(self.port, self.task_queue)
        except zmq.error.ZMQError:
            self.server = None
        self.client = ZMQClient(self.port)

    def update(self):
        """update loop for the ZMQ service; returns any requests
        we have received from other instances"""
        if not self.needs_update():
            raise ValueError("Only call update if this is the server!")
        try:
            item = self.server.requests.get_nowait()
        except Empty:
            return None
        else:
            return Task(item["preset"], item["file"])

    def needs_update(self):
        """returns whether we should call update loop"""
        return self.server is not None


class ZMQServer:
    """
    Server class that waits for other people to connect.
    It writes all requeusts into the queue provided
    """

    def __init__(self, port, task_queue):
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://127.0.0.1:{port}")

        self.requests = task_queue
        self.stopped = threading.Event()
        self.started = False
        self.start()

    def start(self):
        """start the server thread"""
        if self.started:
            raise ValueError("Thread already started!")
        thread = threading.Thread(target=self.thread_func)
        thread.start()
        self.started = True

    def thread_func(self):
        """the endlessly running server thread"""
        while not self.stopped.is_set():
            string = self.socket.recv()
            data = json.loads(string)
            print(f"Received request: [ {data} ]")
            self.requests.put(data)
            self.socket.send_string("received")


class ZMQClient:  # pylint: disable-msg=too-few-public-methods
    """simple client that will send a single message then exit"""

    def __init__(self, port):
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://127.0.0.1:{port}")

    def send(self, preset, file):
        """send a text message"""
        print(f"sending messsage {preset} {file}")
        message = {"preset": preset, "file": file}
        self.socket.send_string(json.dumps(message))
        #  Get the reply.
        message = self.socket.recv()
        print(message)
