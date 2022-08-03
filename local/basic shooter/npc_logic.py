
side = None

def think(obj, enemy, bullets, limit_x:float, mov_speed:int = 5):
    global side
    
    obj_pos = obj.pos
    enemy_pos = enemy.pos
    
    # [+] get closest bullet 
    
    # remove bullets that will not collide
    bullets = bullets.copy()
    bullets.filter(lambda i: (x_len := i.pos.x + i.size.width) < obj_pos.x or x_len > obj_pos.x, )
    
    bullets_in_range : tuple = (*map(lambda i: [obj_pos.y+300, i.pos[1]][i.pos[1] >= obj_pos.y + obj.size.height], bullets),)
    closest_bullet : float = min(bullets_in_range) if len(bullets_in_range) else None
    # [-]
    
    # if no bullet is in range do nothing
    if not closest_bullet:
        # end action
        return 0
    
    # distance between bullet and obj
    distance : float  =  obj_pos.y 
    
    offset = enemy.size.width // 2
     
    # if bullet is a danger, is too close to obj or enemy is "aiming"
    if closest_bullet <= obj_pos.y + (obj.size.height * 2) or enemy_pos.x - offset <= obj_pos.x + obj.size.width and enemy_pos.x + offset >= obj_pos.x:
        
        distance_from_limit = limit_x - obj_pos.x + obj.size.width

        # move to side with more space if not side        
        if not side:
            side = "right" if distance_from_limit > obj_pos.x else "left"
        
        # [+] Manage movement
        
        # move right
        if side == "right":
            # check distance between obj and limit_x
            speed = mov_speed if distance_from_limit > mov_speed else distance_from_limit
            obj_pos.x += speed
            
        # move left
        elif side == "left":
            
            # check distance between obj and limit_x
            speed = mov_speed if obj_pos.x > mov_speed else obj_pos.x
            obj_pos.x -= speed
            
        # [-]
        
        # if obj is in limits change side to None
        if obj_pos.x <= 0 or obj_pos.x >= limit_x:
            side = None
        
        # end action
        return 0
    
            
            

        
        