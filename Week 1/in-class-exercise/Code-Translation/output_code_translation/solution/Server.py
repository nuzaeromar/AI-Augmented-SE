class Server:
    def __init__(self):
        self.white_list = []
        self.send_struct = {}
        self.receive_struct = {}

    def add_white_list(self, addr):
<<<<<<< Updated upstream
=======
        """Add an address to the white list if not already present.
        Returns the updated white list, or an empty list if the address was already present."""
>>>>>>> Stashed changes
        if addr in self.white_list:
            return []
        self.white_list.append(addr)
        return list(self.white_list)

    def del_white_list(self, addr):
<<<<<<< Updated upstream
=======
        """Delete an address from the white list if it exists.
        Returns the updated white list, or an empty list if the address was not found."""
>>>>>>> Stashed changes
        if addr not in self.white_list:
            return []
        self.white_list.remove(addr)
        return list(self.white_list)

    def recv(self, info):
<<<<<<< Updated upstream
        if "addr" not in info or "content" not in info:
            return -1
        addr = int(info["addr"])
=======
        """Process a received message.
        `info` must be a dict containing 'addr' and 'content'.
        Returns:
            -1 if required keys are missing,
             0 if the address is not whitelisted,
             1 on success (updates `receive_struct`)."""
        if not isinstance(info, dict):
            return -1
        if "addr" not in info or "content" not in info:
            return -1
        try:
            addr = int(info["addr"])
        except (ValueError, TypeError):
            return -1
>>>>>>> Stashed changes
        content = info["content"]
        if addr not in self.white_list:
            return 0
        self.receive_struct = {"addr": str(addr), "content": content}
        return 1

    def send(self, info):
<<<<<<< Updated upstream
=======
        """Prepare a message to be sent.
        `info` must be a dict containing 'addr' and 'content'.
        Returns an empty string on success, otherwise an error message."""
        if not isinstance(info, dict):
            return "info structure is not correct"
>>>>>>> Stashed changes
        if "addr" not in info or "content" not in info:
            return "info structure is not correct"
        self.send_struct = {"addr": info["addr"], "content": info["content"]}
        return ""

<<<<<<< Updated upstream
    def show(self, type):
        if type == "send":
            return self.send_struct
        elif type == "receive":
            return self.receive_struct
        else:
            return {}
=======
    def show(self, type_):
        """Return the stored send or receive structure based on `type_`."""
        if type_ == "send":
            return dict(self.send_struct)
        if type_ == "receive":
            return dict(self.receive_struct)
        return {}
>>>>>>> Stashed changes
