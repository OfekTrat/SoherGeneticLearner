
class Agent(object):
    def prepare_data(self, data):
        print("Expecting an Implementation of child agent")
        raise

    def get_signal(self, prepared_data):
        print("Expecting an implementation of child agent")
        raise

    def id(self):
        print("Expecting and implementation of child agent")
        raise

    def _get_int_attrs(self):
        # This function if for the later use of mutating the input attributes of an agent.
        # The in attributes of an agent despite the 'n_outputs' are the ones to mutate.
        list_of_attrs = dir(self)
        int_attrs = []

        for attr in list_of_attrs:
            if type(getattr(self, attr)) == int and attr != "n_outputs":
                int_attrs.append(attr)

        return int_attrs
