
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[],
    OUT invalid_data TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    invalid_list TEXT[] := ARRAY[]::TEXT[];
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        
        IF phones[i] ~ '^[0-9]+$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE name = names[i]) THEN
                UPDATE phonebook SET phone = phones[i] WHERE name = names[i];
            ELSE
                INSERT INTO phonebook(name, phone)
                VALUES (names[i], phones[i]);
            END IF;
        ELSE
            invalid_list := array_append(invalid_list, names[i] || ':' || phones[i]);
        END IF;

    END LOOP;

    invalid_data := invalid_list;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$;
