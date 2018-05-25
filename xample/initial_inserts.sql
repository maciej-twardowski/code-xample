INSERT INTO technology (name) VALUES ("Python"); -- id 1
INSERT INTO technology (name) VALUES ("C++"); -- id 2
INSERT INTO technology (name) VALUES ("Java"); -- id 3

INSERT INTO difficulty (name) VALUES ("easy"); -- id 1
INSERT INTO difficulty (name) VALUES ("medium"); -- id 2
INSERT INTO difficulty (name) VALUES ("hard"); -- id 3

INSERT INTO user (username, password) VALUES ("admin", "admin"); -- id 1
INSERT INTO user (username, password) VALUES ("guest", "guest"); -- id 2
INSERT INTO user (username, password) VALUES ("test", "test"); -- id 3

-- id(A), created(A), likes(A)
-- link_accessible(N), project_name(N), project_author(N)

-- Python Easy
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (1, "xample", "distributed web app assignment", 
    "https://github.com/maciej-twardowski/code-xample", 1, 1);
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (1, "flask", "micro web framework", 
    "https://github.com/pallets/flask", 1, 1);
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (1, "flask debug toolbar", "flask debug toolbar extension", 
    "https://github.com/mgood/flask-debugtoolbar", 1, 1);
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (1, "scikit", "python ml library", 
    "https://github.com/scikit-learn/scikit-learn", 1, 1);
    
-- C++ medium
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (2, "bitcoin", "Bitcoin Core integration/staging tree ", 
    "https://github.com/bitcoin/bitcoin", 2, 2);
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (2, "pytorch", "Tensors and Dynamic neural networks", 
    "https://github.com/pytorch/pytorch", 2, 2);
    
-- Java++ hard
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (3, "elastic search", "RESTful Search Engine", 
    "https://github.com/elastic/elasticsearch", 3, 3);
INSERT INTO post (author_id, title, body, link, technology, difficulty) 
VALUES (3, "guava", "Google core libs for Java", 
    "https://github.com/google/guava", 3, 3);
