FROM ruby:4.0

WORKDIR /code
COPY my-blog/Gemfile .
COPY my-blog/Gemfile.lock .
RUN bundle install --jobs 4
