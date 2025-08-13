FROM ruby:3.3-bullseye

WORKDIR /code
COPY my-blog/Gemfile .
RUN bundle install 