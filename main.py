from conf import key,token
from trello import Trello
import sys
import click


@click.command()
@click.option('--card', prompt="New Card",help='Name for the Card.')
@click.option('--list', prompt='Column of the board',
              help='Name of the list for new card.')
@click.option('--label', prompt='label',
              help='label for new card.')
@click.option('--comment', prompt='comment',
              help='any comment for new card.')

def main(card,list,label,comment):
    """ Include card name, List name, label and comment."""
    test = Trello(key,token)

    board_name_lists = test.get_board_names()

    test.add_member_card(board_name_lists[0],card,list,label,comment)


if __name__ == "__main__":

    main()