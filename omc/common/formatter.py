class Formatter:
    @staticmethod
    def calculate_widths(completions):
        widths = []
        if completions:
            columns = len(completions[0])
            # init columns 
            widths = [0] * columns
            for one_completion in completions:
                for index in range(len(one_completion)):
                    current_width = len(one_completion[index])
                    if current_width > widths[index]:
                        widths[index] = current_width
            return widths

    @staticmethod
    def format_completions(completions, max_width=10, space=2):

        max_widths = Formatter.calculate_widths(completions)
        results = []
        for one in completions:
            results.append(Formatter.format_completion(one, max_widths, max_width=max_width, space=space))

        return results

    @staticmethod
    def format_completion(completion, widths=[], max_width=10, space=2):

        result = ''
        for i in range(0, len(completion)):
            the_value = completion[i]

            width = widths[i] if i < len(widths) else max_width
            if i != 0:
                result = result + the_value.ljust(width + space)
            if i == 0:
                result = result + the_value + ':'

        return result


if __name__ == '__main__':
    completions = [
        ('name', 'address', 'sex', 'first name', 'last name'),
        ('rain', 'biboxuefu', 'male', 'lu', 'ganalin'),
        ('cloud', 'bilinwan', 'female', 'jiang', 'yunyun'),
        ('xiaomi', 'fuligongyu', 'male', 'lu', 'zhihou'),
    ]
    results = Formatter.format_completions(completions)
    print('\n'.join(results))
