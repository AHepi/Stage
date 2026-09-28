# Choices

## Waiting for you

<One numbered question for each open choice, with what happens if the user says nothing.>

## Small choices I made

<One line for each choice taken by default, and how to change it.>

## Answered

<One line for each answered choice and the answer.>

Below this line: details for the AI and the checker. You never need to read them.

### CHOICE <CHOICE- and 3 digits, like CHOICE-021> <a short plain title>
- question: <quick: text>
- why: <quick: text>
- option: <quick, one line each: one word> | text: <text>
- default: <quick: one word> | reason: <text>
- answer: <quick, when choice_answered, the user's answer, set through a choice: an option letter, or text>
- asked: <quick: yes or no>
- checkpoint: <quick: one word from the note>
- affects: <quick: IDs, or <ID>.<field> paths, separated by commas>
- sets: <quick, one line each: <ID>.<field> or CHOICE-NNN-X> | value: <text> | when: <one word>
- locks: <optional: IDs of any record ID, separated by commas>
- based_on: <standard: text>
- status: <quick, code writes it; in a chat without code you write it: open, answered or defaulted>
- date: <quick, code writes it; in a chat without code you write it: year-month-day, or none>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CHOICE: A question for the user with a default; a small choice (asked: no) is grouped under 'small choices I made'. (choice; ID CHOICE- and 3 digits, like CHOICE-021; lives in 01 Choices.md.)
> Allowed values:
> - checkpoint: a, p, b, c, acceptance, d, e, none
> Conditions:
> - choice_answered: CHOICE.status is answered.
> status: open, answered, defaulted.

### SETVALUE <the choice ID, a hyphen and the option letter in capitals, like CHOICE-014-A> <a short plain title>
- target: <quick: a record ID, or the type name of a singleton record or the project (PLAN, STYLE, PROJECT)>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SETVALUE: The full value one option of a CHOICE writes, for answers a sets line cannot hold; code copies its field lines into the target and locks them when that option is chosen. (set value; ID the choice ID, a hyphen and the option letter in capitals, like CHOICE-014-A; lives in 01 Choices.md.)
> status: draft, approved, stale, omitted.
> After target, write the field lines this option sets, exactly as they would appear in the target record.

END OF FILE | Choices | 2 records
