from datetime import datetime


def formatted_date_str(date_str):
    """
    Returns a formatted date string
    :param date_str: date string (e.g. 'YYYY--MM--dd')
    :return: formatted date string
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%d %B, %Y')


def formatted_num_str(num):
    """
    Returns a formatted number string
    :param num: integer
    :return: formatted number string (with units)
    """
    if num >= 1_000_000_000:
        return f'{(num / 1_000_000_000):.1f}b'
    elif num >= 1_000_000:
        return f'{(num / 1_000_000):.1f}m'
    elif num >= 100_000:
        return f'{(num / 1_000):.0f}k'
    else:
        return f'{num:,}'


def main():
    date_str = '2019-10-18'
    formatted = formatted_date_str(date_str)
    print(f"Before: {date_str}")
    print(f"After: {formatted}")

    n1 = 1_346_000_000
    n2 = 1_346_000
    n3 = 345_456
    n4 = 43500
    print(formatted_num_str(n1))
    print(formatted_num_str(n2))
    print(formatted_num_str(n3))
    print(formatted_num_str(n4))


if __name__ == "__main__":
    main()
