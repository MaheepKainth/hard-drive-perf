
TOTAL_NUMBER_OF_TRACKS = 22
TRACK_GROUP = 4
BASE_SECTORS = 8
ADDITIONAL_SECTORS_PER_TRACK_GROUP = 2
HEAD_SPEED = 0.002

THIRTHEENTH_SECTOR = 13
FIRST_TWENTY_FIVE_SECTORS = 25

FOUR_PLACE_VALUES = 5
THREE_PLACE_VALUES = 4
TWO_PLACE_VALUES = 3

DOUBLE_DIGITS = 10
TRIPLE_DIGITS = 100
QUINTUPLE_DIGITS = 10000

RPM_TO_RPS = 60
HALF = 2

ADD_RPM = 1000
ADD_EXTRA_RPM = 2000
ADD_TRACK = 8
MAX_TRACK = 16
TRACK_LOOP = 3
AMOUNT_OF_ROTATION_TIMES_TO_SHOW = 12
RPMS_TO_SHOW = 27

MIN_RPM = 1
MAX_RPM = 50000

FIRST_TRACK = 0

def sectors_in_track(track: int) -> int:
    track_group = (track // TRACK_GROUP)
    sectors = ADDITIONAL_SECTORS_PER_TRACK_GROUP * track_group + BASE_SECTORS
    return sectors

def print_total_sectors() -> int: 
    i = 0
    global total_sectors
    total_sectors = 0
    print('Now displaying the [track #] to [sectors per track] mapping:')
    print('    Track#   #Sectors')
    for i in range(TOTAL_NUMBER_OF_TRACKS): 
        print(f'         {i}        {sectors_in_track(i)}')
        total_sectors += sectors_in_track(i)
    print(f'''
Total # of Sectors: {total_sectors}
          ''')
   
    return total_sectors

def get_total_sectors() -> int:
    i = 0
    global total_sectors
    total_sectors = 0
    for i in range(TOTAL_NUMBER_OF_TRACKS): 
        total_sectors += sectors_in_track(i)
    return total_sectors

def get_sectors_track_num(sector_num: int) -> int:   
    sector_sum = 0
    i = 0
    for i in range(sector_num):   
        sector_sum += sectors_in_track(i)
        if sector_sum > sector_num: break
    return i
        
def test_track_display() -> None:
   
    # sectors per track & total sectors
    print('''TESTING: Track Functions
------------------------''')
    print_total_sectors()
    
    # sector number to track number
    print('''Now displaying the [sector number] to [track number] mapping:
Checking every sector at start.''')
    print('     Sector     Track')
    for i in range(FIRST_TWENTY_FIVE_SECTORS): print(f'          {i}         {get_sectors_track_num(i)}')

    # every 13th sector number to track number
    print('')
    print('Checking every 13th sector.')
    print('     Sector     Track')
    iterable = 0
    for i in range(total_sectors):
        if i == (iterable * THIRTHEENTH_SECTOR) + FIRST_TWENTY_FIVE_SECTORS:
            iterable += 1
            print(f'         {i}         {get_sectors_track_num(i)}')
  
def get_seek_time(starting_track: int, ending_track: int) -> int:
    seek_time = abs(starting_track - ending_track) * HEAD_SPEED
    return seek_time

def test_seek_time() -> None:
    print('''TESTING: Seek Times
-------------------
Now displaying the [track #] to [track #] seek times.
Starting track shown down left most column; ending track in first row
From:      0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21''')
    
    start_track = 0
    for i in range(TOTAL_NUMBER_OF_TRACKS):
        track_times = []
        clean_track_times = ''
        if i < DOUBLE_DIGITS:
            track_times.append(f'    {i}  ')
        else:
            track_times.append(f'    {i} ')
        j = 0
        for j in range(TOTAL_NUMBER_OF_TRACKS):
            
            seek_time = list(str((get_seek_time(start_track, j))))
            
            # for values ending in .000
            if len(seek_time) == FOUR_PLACE_VALUES:
                track_times.append(f'{round(get_seek_time(start_track, j), 3)} ')

            # for values ending in .0x
            elif len(seek_time) == THREE_PLACE_VALUES:
               track_times.append(f'{round(get_seek_time(start_track, j), 3)}0 ')

            # for values ending in .0
            elif len(seek_time) == TWO_PLACE_VALUES:
                track_times.append(f'{round(get_seek_time(start_track, j), 3)}00 ')

            else:
                track_times.append(f'{round(get_seek_time(start_track, j), 3)} ')

        start_track += 1
                
        clean_track_times = ''.join(track_times)
        print(clean_track_times)

def rpm_to_rps(rpm: int) -> float:
    rps = rpm / RPM_TO_RPS
    return rps

def average_rotational_delay(rpm: int) -> float:
    rotational_delay = 1 / (rpm / RPM_TO_RPS) / HALF
    return rotational_delay

def time_to_read_sector(track: int, rpm: int) -> float:
    read_time = 1 / (rpm / RPM_TO_RPS) / sectors_in_track(track)
    return read_time

def test_rotation_times() -> None:
    print('''TESTING: ROTATION TIMES
-----------------------
Now displaying the [rotation delay] per [track].
     RPM       RPS     Rotation Delay     Read Track 1     Read Max Track''')
    
    initial_rpm = 4000
    for i in range(AMOUNT_OF_ROTATION_TIMES_TO_SHOW):
        rotation_delay_per_track = []
        
        # RPM
        if initial_rpm >= QUINTUPLE_DIGITS:
            rotation_delay_per_track.append(f'   {initial_rpm}')
        else:
            rotation_delay_per_track.append(f'    {initial_rpm}')

        # RPS
        if round(rpm_to_rps(initial_rpm), 2) >= TRIPLE_DIGITS:
            rotation_delay_per_track.append(f'    {round(rpm_to_rps(initial_rpm), 2)}')
        else:
            rotation_delay_per_track.append(f'     {round(rpm_to_rps(initial_rpm), 2)}')

        # Rotational Delay
        rotation_delay_per_track.append(f'           {round(average_rotational_delay(initial_rpm), 6)}')

        # Read Track 1
        rotation_delay_per_track.append(f'           {round(time_to_read_sector(0, initial_rpm), 6)}')

        # Read Max Track
        rotation_delay_per_track.append(f'           {round(time_to_read_sector(TOTAL_NUMBER_OF_TRACKS - 1, initial_rpm), 6)}')

        initial_rpm += ADD_RPM

        clean_rotation_delay_per_track = ''.join(rotation_delay_per_track)
        print(clean_rotation_delay_per_track)
        
def average_access_and_read_time(track: int, sector: int, rpm: int) -> float:
    seek_time = get_seek_time(track, get_sectors_track_num(sector))
    rotation_delay = average_rotational_delay(rpm)
    sector_read_time = time_to_read_sector(get_sectors_track_num(sector), rpm)
    return seek_time + rotation_delay + sector_read_time

def average_of_all_read_times(rpm: int) -> float:
    sector = 0
    computations = 0
    time = 0
    track = 0
    for i in range(TOTAL_NUMBER_OF_TRACKS - 1):
        for track in range(sectors_in_track(track)):
            time += average_access_and_read_time(track, sector, rpm)
            sector += 1
            computations += 1
            
            
    time /= computations
    return time

def test_read_times():
    print('''TESTING ACCESS & Read Times
---------------------------
Now displaying time to [access and read] for some sectors for specific 
[RPM], [start track #] and [target sector #].
       RPM     Track     Sector        Time''')
    change_rpm = 9
    change_track = 3
    rpm = 4000
    track = 0
    sector = 0
    loop_num = 0
    track_loop_num = 0
    rpm_loop = 1
    sector_loop = 0
    for i in range(RPMS_TO_SHOW):
        access_and_read_time = []
        
        if sector_loop == 0:
            sector_loop += 1
            sector = 0
        elif sector_loop == 1:
            sector_loop += 1
            sector = 123
        elif sector_loop == 2:
            sector_loop = 0
            sector = 246

        #RPM
        access_and_read_time.append(f'      {rpm}')
        
        #TRACK
        if track > DOUBLE_DIGITS:
            access_and_read_time.append(f'        {track}')
        else:
            access_and_read_time.append(f'         {track}')
        
        #SECTOR
        if sector > TRIPLE_DIGITS:
            access_and_read_time.append(f'        {sector}')
        else:
            access_and_read_time.append(f'          {sector}')

        #TIME
        access_and_read_time.append(f'    {round(average_access_and_read_time(track, sector, rpm), 6)}')

        loop_num += 1
        track_loop_num += 1

        if loop_num == change_rpm:
            rpm_loop += 1
            change_rpm *= rpm_loop
            rpm += ADD_EXTRA_RPM

        if track_loop_num == change_track:
            change_track += TRACK_LOOP
            track += ADD_TRACK
            if track > MAX_TRACK:
                change_track = 3
                track = 0
                track_loop_num = 0

        clean_access_and_read_time = ''.join(access_and_read_time)
        print(clean_access_and_read_time)

def display_hard_drive_statistics() -> int:
    rpm = int(input('Enter HD rotations per minute (RPM) : '))
    while True:
        if rpm < MIN_RPM or rpm > MAX_RPM:
            print('Error: Value must be between 1 and 50000.')
            rpm = int(input('Enter HD rotations per minute (RPM) : '))
        else:
            break
    
    print(f'''
Hard Drive Statistics:
---------------------
Number of tracks:             {TOTAL_NUMBER_OF_TRACKS}
Total number of sectors:      {get_total_sectors()}
Revolutions per minute (RPM): {rpm}
Revolutions per second (RPS): {round(rpm_to_rps(rpm), 1)}
Rotational delay (seconds):   {round(average_rotational_delay(rpm), 6)}
Time to read first sector:    {round(time_to_read_sector(FIRST_TRACK, rpm), 6)}
Time to read last sector:     {round(time_to_read_sector(TOTAL_NUMBER_OF_TRACKS, rpm), 6)}
Average read time:            {round(average_of_all_read_times(rpm), 6)}''')
    
def main():
    test_track_display()
    test_seek_time()
    test_rotation_times()
    test_read_times()
    display_hard_drive_statistics()

main()