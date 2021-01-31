import json

# todo@rain
# 1. pre-calculate resource spec for strategy patch merge
# 2. calcuate for resource completion


if __name__ == '__main__':
    content = {}
    with open('/Users/luganlin/git/mf/omc/omc/fixtures/k8s/swagger.json') as f:
        content = json.load(f)

    for k,v in content['definitions'].items():
        print(k)


