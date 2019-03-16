


def test(run_rate):
    kirat = Player('Kirat Boli', run_rate, 4)
    x = [kirat.bat() for i in range(1, 1000)]
    return sum(x) / 1000


if __name__ == '__main__':
    team_bangalore = Team("bangalore", [
        Player('Kirat Boli', 30, 4), Player('NS Nodhi', 10), Player('R Rumrah', 9),
        Player('Shashi Henra', 6)
    ], wickets_left)

    team_chennai = Team("chennai", [], 0)
    umpire = Umpire()
    game = Game(team_bangalore, team_chennai, umpire, overs_left)

    observer = Observer()
    commentator = Commentator()
    observers = [observer, commentator]
    game.add_observers(observers)
    winner = game.play()

    print(observer.summarize_match())
    print(commentator.commentary())
    # Player('x', 37)
    # print([(i, test(i)) for i in range(6, 37)])
