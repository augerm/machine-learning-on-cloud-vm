import argparse
import os

from NeuralNet import NeuralNet

def main():
    parser = argparse.ArgumentParser(description='Train a model.')
    parser.add_argument('--csv')
    parser.add_argument('--out_dir')
    parser.add_argument('--param_dir')

    args = parser.parse_args()
    csv_location = os.path.join(os.getcwd(), args.csv)
    out_dir = os.path.join(os.getcwd(), args.out_dir)
    param_file = args.param_dir
    neural_net = NeuralNet(csv_location, out_dir, param_file)
    neural_net.train()
    neural_net.save()

if __name__ == "__main__":
    main()