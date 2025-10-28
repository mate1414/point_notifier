class DeliveryStrategy:
    def __init__(self, channels):
        self.channels = channels
        self.current_index = 0

    def get_next_channel(self):
        if self.current_index < len(self.channels):
            channel = self.channels[self.current_index]
            self.current_index += 1
            return channel
        return None

    def has_next(self):
        return self.current_index < len(self.channels)