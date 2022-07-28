"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from dialogue import dh
import inflect
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

INTRO, CHOOSE_SOLUTION, CHOOSE_VOTE, CHOOSE_FAIR, TYPING_SOLUTION, TYPING_FAIR, RESPONSE_SIMILAR, RESPONSE_OPPOSITE, VOTING_SOLUTION = range(9)

p = inflect.engine()

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and ensure that the user read the intro."""
    reply_keyboard = [['Okay. Let\'s start.']]

    update.message.reply_text('Welcome \U0001F603')
    update.message.reply_text(
        'Today, we will discuss how to resolve ' + p.number_to_words(len(dh.needs)) + ' conflicts.'
    )
    update.message.reply_text('For each conflict, there are two groups with opposing needs, one of which includes yours.')
    update.message.reply_text(
        'I will ask your ideas for resolving each conflict that are most productive and fair to both groups.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        ),
    )

    return INTRO


def intro(update: Update, context: CallbackContext) -> int:
    """Introduce a conflict"""
    reply_keyboard = [['Yes.', 'No.']]

    conflict = 'In the ' + p.number_to_words(p.ordinal(dh.conflict_index + 1)) \
               + ' conflict, \n' + dh.needs[dh.conflict_index][0] \
               + ', while ' + dh.needs[dh.conflict_index][1] + '.'

    update.message.reply_text(conflict, parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('What do you think about this conflict?')
    update.message.reply_text(
        'In principal, do you think it is feasible to design the course that satisfies both groups?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='')
    )

    return CHOOSE_SOLUTION


def typing_solution(update: Update, context: CallbackContext) -> int:
    """Ask how designing a course would be possible"""
    update.message.reply_text(
        'Great! What do you suggest?',
        reply_markup=ReplyKeyboardRemove()
    )

    return TYPING_SOLUTION


def choose_vote(update: Update, context: CallbackContext) -> int:
    """Ask whether voting is what the user want"""
    reply_keyboard = [['Yes.', 'No.']]

    update.message.reply_text(
        'I see. Then, perhaps we should take a vote and decide which group to satisfy?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='')
    )

    return CHOOSE_VOTE


def choose_fair(update: Update, context: CallbackContext) -> int:
    """Ask whether the approach would be fair to the others"""
    reply_keyboard = [['Yes.', 'Maybe.', 'No.']]

    if update.message.text == 'Yes.':
        dh.current_direction = 'vote'
        dh.personal_idea = '\"Take a vote and decide which group to satisfy.\"'
    else:
        dh.current_direction = 'solution'
        dh.personal_idea = update.message.text

    update.message.reply_text(
        'Interesting. Do you think your approach is fair to both groups?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='')
    )

    return CHOOSE_FAIR


def typing_fair(update: Update, context: CallbackContext) -> int:
    """Ask why the approach would be (un)fair"""
    update.message.reply_text(
        'I see. Why do you think like that?',
        reply_markup=ReplyKeyboardRemove(),
    )

    return TYPING_FAIR


def response_similar(update: Update, context: CallbackContext) -> int:
    """Present similar approach"""
    reply_keyboard = [['I see.']]

    rationale_similar = ''
    approach = ''

    if dh.current_direction == 'solution':
        rationale_similar = dh.ideas[dh.conflict_index][0] + '\n' \
                            + dh.ideas[dh.conflict_index][1] + '\n' \
                            + dh.ideas[dh.conflict_index][2]
        approach = '*designing the course to satisfy both groups* such as:'
    elif dh.current_direction == 'vote':
        rationale_similar = dh.votes[dh.conflict_index][0] + '\n' \
                            + dh.votes[dh.conflict_index][1] + '\n' \
                            + dh.votes[dh.conflict_index][2]
        approach = '*voting* because:'

    update.message.reply_text('Thank you for sharing your thoughts.')
    update.message.reply_text(
        'Similarly, other students have suggested ' + approach,
        parse_mode=ParseMode.MARKDOWN
    )
    update.message.reply_text(
        rationale_similar,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
        )
    )

    return RESPONSE_SIMILAR


def response_opposite(update: Update, context: CallbackContext) -> int:
    """Present opposite approach"""
    rationale_opposite = ''
    approach = ''
    opposite_approach = ''

    if dh.current_direction == 'solution':
        rationale_opposite = dh.votes[dh.conflict_index][0] + '\n' \
                            + dh.votes[dh.conflict_index][1] + '\n' \
                            + dh.votes[dh.conflict_index][2]
        approach = '*voting to satisfy one of the groups* because:'
        opposite_approach = '*voting*'
    elif dh.current_direction == 'vote':
        rationale_opposite = dh.ideas[dh.conflict_index][0] + '\n' \
                            + dh.ideas[dh.conflict_index][1] + '\n' \
                            + dh.ideas[dh.conflict_index][2]
        approach = '*designing the course to satisfy both groups* such as:'
        opposite_approach = '*designing the course to satisfy both groups*'

    update.message.reply_text(
        'In contrast, some students suggested ' + approach,
        parse_mode=ParseMode.MARKDOWN,
    )
    update.message.reply_text(rationale_opposite)
    update.message.reply_text(
        'If you need to support ' + opposite_approach + ', how would you convince the others?',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )

    return RESPONSE_OPPOSITE


def voting_solution(update: Update, context: CallbackContext) -> int:
    """Move on to the next conflict"""
    reply_keyboard = [['1', '2', '3', '4', '5']]
    second_suggestion = update.message.text

    if dh.personal_idea == '\"Take a vote and decide which group to satisfy.\"':
        vote_items = '1: "Voting to satisfy one of the groups."\n\n' + \
                    '2: "' + second_suggestion + '"\n\n' + \
                    '3: ' + dh.votes[dh.conflict_index][0] + '\n' + \
                    '4: ' + dh.votes[dh.conflict_index][1] + '\n' + \
                    '5: ' + dh.votes[dh.conflict_index][2] + '\n'
    else:
        vote_items = '1: "' + dh.personal_idea + '"\n\n' + \
                     '2: ' + dh.ideas[dh.conflict_index][0] + '\n' + \
                     '3: ' + dh.ideas[dh.conflict_index][1] + '\n' + \
                     '4: ' + dh.ideas[dh.conflict_index][2] + '\n' + \
                     '5: "Voting to satisfy one of the groups."\n'

    update.message.reply_text('Interesting suggestion!')
    update.message.reply_text('I will share it with other participants next time they log in \U0001F603')
    update.message.reply_text(
        'Now, please select the approach that is most productive and fair to both groups in your perspective.\n\n'
        + vote_items,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='I vote for...'
        )
    )

    return VOTING_SOLUTION


def nextConflict(update: Update, context: CallbackContext) -> int:
    """Move on to the next conflict"""
    reply_keyboard = [['Okay. Let\'s start.']]

    if dh.conflict_index >= 1:
        user = update.message.from_user
        logger.info("User %s completed the conversation.", user.first_name)
        update.message.reply_text('Thank you for sharing your thoughts!')
        update.message.reply_text(
            'I added your vote to the group decision on how to resolve this conflict.',
            reply_markup=ReplyKeyboardRemove(),
        )
        update.message.reply_text('This is the end of the discussion today.')
        update.message.reply_text('I will contact you again when everyone complete sharing their thoughts. Bye!')

        return ConversationHandler.END
    else:
        update.message.reply_text('Great!')
        update.message.reply_text('I added your vote to the group decision on how to resolve this conflict.')
        update.message.reply_text(
            'Let’s move on to the next conflict.',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder=''
            ),
        )
        dh.conflict_index += 1
        return INTRO


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("token")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states e.g., INTRO, CHOOSE_SOLUTION, CHOOSE_VOTE...
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INTRO: [MessageHandler(Filters.regex('^Okay. Let\'s start.$'), intro)],
            CHOOSE_SOLUTION: [
                MessageHandler(Filters.regex('^Yes.$'), typing_solution),
                MessageHandler(Filters.regex('^No.$'), choose_vote)
            ],
            CHOOSE_VOTE: [
                MessageHandler(Filters.regex('^Yes.$'), choose_fair),
                MessageHandler(Filters.regex('^No.$'), intro)
            ],
            CHOOSE_FAIR: [MessageHandler(Filters.regex('^(Yes.|Maybe.|No.)$'), typing_fair)],
            TYPING_SOLUTION: [MessageHandler(Filters.text & ~Filters.command, choose_fair)],
            TYPING_FAIR: [MessageHandler(Filters.text & ~Filters.command, response_similar)],
            RESPONSE_SIMILAR: [MessageHandler(Filters.regex('^I see.$'), response_opposite)],
            RESPONSE_OPPOSITE: [MessageHandler(Filters.text & ~Filters.command, voting_solution)],
            VOTING_SOLUTION: [MessageHandler(Filters.text & ~Filters.command, nextConflict)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('intro', intro),
            CommandHandler('suggest', typing_solution),
            CommandHandler('fair', choose_fair),
            CommandHandler('why', typing_fair),
            CommandHandler('perspective', response_opposite),
            CommandHandler('vote', voting_solution),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
