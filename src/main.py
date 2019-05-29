import argparse
import yaml

from restler import *
from request.generator import Generator
from swagger.parser import SwaggerParser
from utils.config_utils import *
from utils.yaml_utils import read_yaml_file


def get_req_set(doc):
  parser = SwaggerParser(doc)
  return parser.get_req_set()

def read_params(params):
  doc,    errno1 = read_yaml_file(params.target)
  config, errno2 = read_yaml_file(params.config)
  if errno1 == -1 or errno2 == -1:
    print("[*] Program exits...")
    exit(0)
  return doc, config

def main(params):
  doc, config = read_params(params)
  max_length = get_max_length(config)
  req_set = get_req_set(doc)
  for i in req_set:
    generator = Generator(i)
    ret = generator.get_message()
    print (ret)

  # REST-ler method
  n = 1
  bfs = BFS(req_set)
  #bfsfast = BFSFast(req_set)
  #randomwalk = RandomWalk(req_set)

  while n <= max_length:
    seq_set = bfs.search(n)
    #seq_set = render(seq_set, seq_set)
    n = n + 1

  # NPFuzz
  pass


if __name__ == '__main__':
  """ Welcome to "NP Fuzz" which is a REST API Fuzzing with State Diversity.

      This program must need
        1) *.yaml which is a swagger yaml file of target
        2) config.yaml

      For example:
        $ python main.py --target swagger.yaml --config config.yaml

      If you want to know how to use this program, command:
        $ python main.py --help
  """
  parser = argparse.ArgumentParser(
                            description='REST API Fuzzing with State Diversity')
  parser.add_argument('--target', required=True, metavar='*.yaml',
                                  help='swagger yaml file of target')
  parser.add_argument('--config', required=True, metavar='config.yaml',
                                  help='configuration file')
  exit(main(parser.parse_args()))
