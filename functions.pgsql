CREATE OR REPLACE FUNCTION get_listener_hours ( start_timestamp timestamptz, end_timestamp timestamptz ) RETURNS numeric AS $$
DECLARE
    listener_hours NUMERIC;
BEGIN
    SELECT INTO
        listener_hours
        (round(sum(log.bytes) / 1024::numeric / max(mount_points.bitrate)::numeric / (60 * 60)::numeric, 2))
    FROM 
        log 
    JOIN 
        mount_points 
    ON 
        log.mount_point_id = mount_points.id
    WHERE 
        timestamp > start_timestamp
    AND
        timestamp < end_timestamp
    AND mount_points.mount_point = mount_point
    GROUP BY 
        mount_points.mount_point;
    RETURN listener_hours;
END;
$$ LANGUAGE plpgsql;