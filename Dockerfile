FROM ruby:4.0.1-bookworm

WORKDIR /code
COPY my-blog/Gemfile .
COPY my-blog/Gemfile.lock .
RUN bundle install