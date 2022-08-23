CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);


CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);


CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

CREATE TABLE tag (
    id serial NOT NULL,
    name text
);



