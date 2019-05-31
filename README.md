## Introduction

TL;DR

Extend CloudFormation templates produced by [cfhighlander](https://github.com/theonestack/cfhighlander.git)

1. Compile the tempate and publish to s3
```
$ docker run --rm -it -v $PWD:/src -w /src \
    -v $HOME/.aws:/home/cfhighlander/.aws theonestack/cfhighlander bash

$ cfpublish github:toshke/cfhl-component-cfhlmacros

```

2. Create a CloudFormation stack using Console url from the output

```
...
Use following url to launch CloudFormation stack

https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?filter=active&templateURL=https://123456789012.us-east-1.cfhighlander.templates.s3.amazonaws.com/published-templates/cfhlmacros/latest/cfhlmacros.compiled.yaml&stackName=cfhlmacros

...
```

3. Use `Cfhighlander_Networking` macro like following in your template, to read [vpc component subnets](https://github.com/theonestack/hl-component-vpc)
