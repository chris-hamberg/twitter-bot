INSERT INTO user (id, name, username) VALUES (0, 'Taco',    'Bell');
INSERT INTO user (id, name, username) VALUES (1, 'Bob',     'Bell');
INSERT INTO user (id, name, username) VALUES (2, 'Luke',    'Skywalker');
INSERT INTO user (id, name, username) VALUES (3, 'Brandon', 'Obama');
INSERT INTO user (id, name, username) VALUES (4, 'Wendy',   'Hamburger');

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower', 0);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower', 1);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower', 2);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower', 3);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'followingQ', 3);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'followingQ', 4);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'blacklist', 1);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'friendQ',   2);

INSERT INTO user_s (admin, id) VALUES (12345, 0);
INSERT INTO user_s (admin, id) VALUES (12345, 2);
INSERT INTO user_s (admin, id) VALUES (12345, 3);
INSERT INTO user_s (admin, id) VALUES (12345, 4);
INSERT INTO user_s (admin, id, unfollowed_count) VALUES (12345, 1, 3);
