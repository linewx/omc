import os

header = ['pid', 'username', 'pri', 'nice', 'size', 'res', 'state', 'time', 'wcpu', 'cpu', 'processname', 'session',
          'table', 'client', 'command']


def parse_pg_top(filename):
    with open(filename) as f:
        all_lines = f.readlines()
        start = False
        for one_line in all_lines:

            striped_line = one_line.strip()
            if striped_line.startswith("PID"):
                start = True
                continue

            if not start:
                continue

            result = striped_line.split(None, 14)
            yield dict(zip(header, result))


def parse_pg_top_summary(filename):
    '''Message parser
    last pid: 13501;  load avg:  1.51,  1.97,  2.04;       up 0+02:48:55   11:54:47
467 processes: 13 running, 454 sleeping
CPU states: 41.3% user,  0.0% nice,  4.7% system, 54.0% idle,  0.0% iowait
Memory: 13G used, 18G free, 1292K buffers, 2337M cached
DB activity: 2757 tps,  2 rollbs/s,   3 buffer r/s, 99 hit%,  10369 row r/s,  252 row w/s
DB I/O:     0 reads/s,     0 KB/s,     0 writes/s,     0 KB/s
DB disk: 110.5 GB total, 104.1 GB free (5% used)
Swap: 8192M free
    '''
    with open(filename) as f:
        summary = {}
        all_lines = f.readlines()
        for one_line in all_lines:

            striped_line = one_line.strip()
            if striped_line.startswith("Memory"):
                import re
                a = re.search("(\d*)G free", striped_line)
                summary['free'] = int(a.groups()[0])
                if summary.get('free') is None:
                    print(filename)
                break

        return summary


def is_active(item):
    if item.get('state') == 'run' or (item.get('command') is not None and not item.get('command').endswith('idle')):
        return True


def analyze_result(result):
    summary = {
        'active': 0,
        'lines': 0

    }
    active_count = 0
    lines = 0
    for item in result:
        if is_active(item):
            active_count += 1
        lines = lines + 1

    summary['active'] = active_count
    summary['lines'] = lines
    return summary


if __name__ == '__main__':
    summary = {
        'active_file_name': '',
        'active_count': 0,
        'lines_file_name': '',
        'lines_count': 0,
        'free_file_name': '',
        'free_count': 30
    }
    the_file_name = ''
    count = 0
    for filename in os.listdir("/tmp/pgreport/pgreport"):
        result = parse_pg_top(os.path.join('/tmp/pgreport/pgreport', filename))
        the_result = analyze_result(result)
        active_count = the_result.get('active')
        lines_count = the_result.get('lines')

        if active_count > summary.get('active_count'):
            summary['active_count'] = active_count
            summary['active_file_name'] = filename

        if lines_count > summary.get('lines_count'):
            summary['lines_count'] = lines_count
            summary['lines_file_name'] = filename

        summary_result = parse_pg_top_summary(os.path.join('/tmp/pgreport/pgreport', filename))
        if summary_result.get('free') < summary.get('free_count'):
            summary['free_file_name'] = filename
            summary['free_count'] = summary_result.get('free')

    print(summary)
