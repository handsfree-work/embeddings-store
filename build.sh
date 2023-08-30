#!/bin/bash
set -e
echo "请先输入一个版本号(like 1.0.0)："
read version

echo "您输入的版本号是： $version"
echo "登录aliyun镜像仓库"
sudo docker login --username=252959493@qq.com registry.cn-shenzhen.aliyuncs.com

sudo -E docker compose build
sudo -E docker compose push
