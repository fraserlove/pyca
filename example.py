if __name__ == '__main__':
    from pyca import BriansBrain, GameOfLife, LangtonsAnt, PredatorPrey, WireWorld

    # Create and run a randomised instance of Conway's Game of Life
    GameOfLife()

    # Create and run a instance of Wire World from a RLE file
    WireWorld('grids/wire_world/circuit.ca')