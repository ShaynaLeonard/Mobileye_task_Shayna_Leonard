from typing import List
import json

expected_messages_frequency = {
    1:1,
    9:48,
    18:84,
    36:164
}

class Solution:
    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path

    def check(self):
        try:
            with open (self.data_file_path, "r") as f:
                pass
            with open(self.protocol_json_path, "r") as f:
                pass
        except FileNotFoundError:
            print(f"Error: The file '{self.data_file_path}' was not found.")
        except PermissionError:
            print(f"Error: Permission denied when trying to open '{self.data_file_path}'.")
        except IsADirectoryError:
            print(f"Error: Expected a file but found a directory: '{self.data_file_path}'.")
        except IOError as e:
            print(f"Error: An I/O error occurred: {e}")
        except Exception as e:
            # This captures any other exceptions not caught by the above
            print(f"An unexpected error occurred: {e}")


    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        try:
            with open (self.data_file_path, "r") as f:
                line = f.readline().split(",")
                if len(line) >= 5:
                    hex_values = line[4].split()
                    ascii_characters = [chr(int(hv, 16)) for hv in hex_values]
                    return ''.join(ascii_characters)
                else:
                    return f"Version name doesn't exist!"
        except FileNotFoundError:
            print(f"Error: The file '{self.data_file_path}' was not found.")
        except PermissionError:
            print(f"Error: Permission denied when trying to open '{self.data_file_path}'.")
        except IsADirectoryError:
            print(f"Error: Expected a file but found a directory: '{self.data_file_path}'.")
        except IOError as e:
            print(f"Error: An I/O error occurred: {e}")
        except Exception as e:
            # This captures any other exceptions not caught by the above
            print(f"An unexpected error occurred: {e}")

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        global expected_messages_frequency
        # TODO: error id doesnt exist
        protocol = {}
        not_matching = []
        try:
            # Counting the appearances of each protocol
            with open (self.data_file_path, "r") as f:
                for line in f:
                    words = line.split(",")
                    if len(words)<3:
                        print(f"There is no protocol, continuing...")
                        continue
                    protocol_id = words[2].strip()
                    if protocol_id in protocol:
                        protocol[protocol_id] +=1
                    else:
                        protocol[protocol_id ] = 1

            # Checking if the amount of the appearances matches the map
            with open(self.protocol_json_path, "r") as file:
                protocol_data = json.load(file)
                for key, value in protocol.items():
                    if key in protocol_data.get("protocols"):
                        fps = protocol_data.get("protocols").get(key).get("fps")
                        if fps not in expected_messages_frequency:
                            print(f"The fps {fps} in protocol {key} isn't in the fps-message frequency map")
                            continue
                        if value != expected_messages_frequency[fps]:
                            not_matching.append(key)
                    else:
                        print(f"ID {key} in session isn't found in the protocol json")
                        continue
            return not_matching
        except FileNotFoundError:
            print(f"Error: The file '{self.data_file_path}' was not found.")
        except PermissionError:
            print(f"Error: Permission denied when trying to open '{self.data_file_path}'.")
        except IsADirectoryError:
            print(f"Error: Expected a file but found a directory: '{self.data_file_path}'.")
        except IOError as e:
            print(f"Error: An I/O error occurred: {e}")
        except Exception as e:
            # This captures any other exceptions not caught by the above
            print(f"An unexpected error occurred: {e}")

    def create_protocol_set_from_json(self):
        '''
        This method creates a protocol set from the protocol json file
        :return: set
        '''
        try:
            version_name = self.q1()
            with open(self.protocol_json_path, "r") as protocol_file:
                protocol_data = json.load(protocol_file)
                if version_name in protocol_data.get("protocols_by_version"):
                    if protocol_data.get("protocols_by_version").get(version_name).get("id_type") == "dec":
                        protocol_set = set()
                        for decimal in protocol_data.get("protocols_by_version").get(version_name).get("protocols"):
                            hex_value = hex(int(decimal.strip()))
                            protocol_set.add(hex_value)
                    else:
                        protocol_set = set(protocol_data.get("protocols_by_version").get(version_name).get("protocols").strip())
                else:
                    print(f"Version name {version_name} isn't in the protocol data file")
                    return []
            return protocol_set

        except FileNotFoundError:
            print(f"Error: The file '{self.data_file_path}' was not found.")
        except PermissionError:
            print(f"Error: Permission denied when trying to open '{self.data_file_path}'.")
        except IsADirectoryError:
            print(f"Error: Expected a file but found a directory: '{self.data_file_path}'.")
        except IOError as e:
            print(f"Error: An I/O error occurred: {e}")
        except Exception as e:
            # This captures any other exceptions not caught by the above
            print(f"An unexpected error occurred: {e}")

    def create_protocol_set_from_data(self):
        protocols_in_session = set()
        try:
            with open(self.data_file_path, "r") as data_file:
                for line in data_file:
                    words = line.split(",")
                    if len(words) < 3:
                        print(f"There is no protocol, continuing...")
                        continue
                    else:
                        protocols_in_session.add(words[2].strip())
            return protocols_in_session

        except FileNotFoundError:
            print(f"Error: The file '{self.data_file_path}' was not found.")
        except PermissionError:
            print(f"Error: Permission denied when trying to open '{self.data_file_path}'.")
        except IsADirectoryError:
            print(f"Error: Expected a file but found a directory: '{self.data_file_path}'.")
        except IOError as e:
            print(f"Error: An I/O error occurred: {e}")
        except Exception as e:
            # This captures any other exceptions not caught by the above
            print(f"An unexpected error occurred: {e}")

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self) -> List[str]:
        protocols_in_json = self.create_protocol_set_from_json()
        protocols_in_session = self.create_protocol_set_from_data()
        missing = protocols_in_json - protocols_in_session
        return list(missing)

    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self) -> List[str]:
        protocols_in_json = self.create_protocol_set_from_json()
        protocols_in_session = self.create_protocol_set_from_data()
        missing = protocols_in_session - protocols_in_json
        return list(missing)

    def hex_length_in_bytes(self, hex_string):
        hex_string = hex_string.replace(" ", "")
        num_hex_digits = len(hex_string)
        num_bytes = (num_hex_digits + 1) // 2
        return num_bytes

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        #TODO - edge case 0 bytes
        protocols = []
        try:
            with open(self.data_file_path, "r") as data_file:
                for line in data_file:
                    words = line.split(",")
                    bytes_count = int(words[3].split()[0])
                    if len(words) < 5: #there is no message at all
                        if bytes_count != 0:
                            protocols.append(words[2].strip())
                    else:
                        bytes_in_message = self.hex_length_in_bytes(words[4])-1
                        if bytes_in_message != bytes_count:
                            protocols.append(protocols.append(words[2].strip()))
            return protocols

        except FileNotFoundError:
            print(f"Error: The file '{self.data_file_path}' was not found.")
        except PermissionError:
            print(f"Error: Permission denied when trying to open '{self.data_file_path}'.")
        except IsADirectoryError:
            print(f"Error: Expected a file but found a directory: '{self.data_file_path}'.")
        except IOError as e:
            print(f"Error: An I/O error occurred: {e}")
        except Exception as e:
            # This captures any other exceptions not caught by the above
            print(f"An unexpected error occurred: {e}")


    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        pass

if __name__ == "__main__":
    sol = Solution("data.txt", "protocol.json")
    print(sol.q5())
