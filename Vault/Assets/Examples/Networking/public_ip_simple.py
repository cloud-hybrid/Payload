#!/usr/bin/env python

from requests import get

def get_ip():
  ip = get('https://api.ipify.org').text

  return ip

def main():
  public_ip = get_ip()

  print(public_ip)

if __name__ == "__main__":
  main()