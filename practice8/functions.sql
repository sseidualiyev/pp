CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS
$$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name::TEXT, pb.phone::TEXT
    FROM phonebook pb
    WHERE pb.name ILIKE '%' || pattern || '%'
       OR pb.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS
$$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name::TEXT, pb.phone::TEXT
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;