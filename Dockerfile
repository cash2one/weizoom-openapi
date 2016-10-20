#消息队列 images
FROM reg.weizzz.com:5000/wz/redmine-agent:1.0
MAINTAINER  "fanweiming@weizoom.com"

RUN easy_install supervisor &&\
easy_install -U git+https://git2.weizzz.com:84/microservice/mns_python_sdk.git &&\
easy_install -U git+https://git2.weizzz.com:84/microservice/dingtalk-sso.git &&\
easy_install -U git+https://git2.weizzz.com:84/microservice/eaglet.git &&\
easy_install django\  
&& rm -rf ~/.pip ~/.cache

RUN mkdir -p /service

ADD . /service

WORKDIR /service

CMD ["/usr/local/bin/dumb-init", "/bin/bash", "start_service.sh"]
