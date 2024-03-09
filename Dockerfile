FROM jekyll/jekyll:4

WORKDIR /code
COPY site/Gemfile .
RUN bundle install 