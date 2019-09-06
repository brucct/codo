FROM ss1917/codo_base:beta0.3

#
RUN pip3 install --upgrade pip
RUN pip3 install -U git+https://github.com/ss1917/ops_sdk.git

# 复制代码
RUN mkdir -p /var/www/
ADD . /var/www/codo-admin/

# 安装pip依赖
RUN pip3 install -r /var/www/codo-admin/doc/requirements.txt

# 日志
VOLUME /var/log/

#准备文件
COPY doc/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY doc/supervisor_ops.conf  /etc/supervisord.conf

EXPOSE 80
CMD ["/usr/bin/supervisord"]
