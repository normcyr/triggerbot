#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import praw
import yaml
import logging.config
import os


def setup_logging(logging_config_file, env_key = 'LOGGING'):

    path = logging_config_file
    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)
        logging.getLogger(__name__)
        logging.Logger(True)

    else:
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(name)s - %(message)s')
        logging.debug('No logging configuration found. Using the default settings.')


def read_config(config_file):

    with open(config_file, 'r') as f:
        config_dict = yaml.safe_load(f)
        logging.info('Reading the bot\'s configuration file')

    return(config_dict)


def init_reddit_bot(config_dict):

    logging.info('Logging in to Reddit')
    reddit_bot = praw.Reddit(client_id = config_dict['bot']['client_id'],
                    client_secret = config_dict['bot']['client_secret'],
                    user_agent = config_dict['bot']['user_agent'],
                    username = config_dict['user']['user_name'],
                    password = config_dict['user']['password']
                    )

    if reddit_bot.user.me() == config_dict['user']['user_name']:
            logging.info('Logged in to Reddit')
            return(reddit_bot)

    else:
        logging.info('Problem logging in to Reddit')


def make_trigger_dict(trigger_text_basepath, config_dict):

    trigger_text_dict = {}

    for trigger_word in config_dict['trigger_words']:

        filename = trigger_text_basepath + trigger_word[1:] + '.md'

        with open(filename, 'r') as f:

            trigger_text_dict[trigger_word] = [f.read()]
            logging.info('Reading the text from {} for the trigger word {}'.format(filename, trigger_word))

    return(trigger_text_dict)


def read_last_comments(reddit_bot, config_dict, trigger_text_dict):

    logging.info('Reading the last 10 comments')

    for comment in reddit_bot.subreddit(config_dict['subreddit']).comments(limit=10):

        for trigger_word in config_dict['trigger_words']:

            if trigger_word in comment.body:

                parent_id = comment.parent().id
                logging.info('Trigger word found: {}. Corresponding comment\'s parent ID is: {}.'.format(trigger_word, comment.parent().id))

                already_answered = check_if_already_answered(reddit_bot, config_dict, parent_id)

                if already_answered == True:
                    logging.info('Trigger word was already answered by the bot, moving on.')
                else:
                    logging.info('Trigger word was not answered by the bot!')
                    post_bot_comment(trigger_text_dict, trigger_word, comment)


def check_if_already_answered(reddit_bot, config_dict, parent_id):

    logging.info('Checking if it was already anwsered')
    list_authors = []
    parent_submission = reddit_bot.submission(id = parent_id)

    for comment in parent_submission.comments:
        list_authors.append(comment.author)

    if config_dict['user']['user_name'] in list_authors:
        already_answered = True
    else:
        already_answered = False

    return(already_answered)


def post_bot_comment(trigger_text_dict, trigger_word, comment):

    logging.info('Posting the comment corresponding to the trigger word {}.'.format(trigger_word))
    comment.parent().reply(trigger_text_dict[trigger_word])


def main():

    config_file = 'triggerbot/config/config.yml'
    logging_config_file = 'triggerbot/config/logging.yml'
    trigger_text_basepath = 'triggerbot/trigger_text/'
    
    setup_logging(logging_config_file)

    config_dict = read_config(config_file)

    trigger_text_dict = make_trigger_dict(trigger_text_basepath, config_dict)

    reddit_bot = init_reddit_bot(config_dict)

    read_last_comments(reddit_bot, config_dict, trigger_text_dict)


if __name__ == '__main__':
    main()
