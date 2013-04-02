#!/usr/bin/ruby
#
# Copyright (C) 2013 Tim Strazzere - diff@lookout.com
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Decoder for Kakabet.a - targeted malware against Tibetian activists
# Tested and used for sample;
#  SHA1:   s495b622d8209820022fe743c340b39e6e9313cd9
#  SHA256: 9390a145806157cadc54ecd69d4ededc31534a19a1cebbb1824a9eb4febdc56d

# Got to love the sense of humor and life advice...
DECODE_KEY = "marriage and parenting are serious commitments dont be in a hurry"                                                                                                                                                          
printf "[*] Kakabet decoder - Tim Strazzere - diff@lookout.com\n"

if(ARGV.length != 1)
  printf " [!] Expecting one argument - exiting\n"
  exit
end

File.open(ARGV[0]) do |f|
  string = f.read

  # Kill the buffer in the front and back if it exists
  if(string.start_with?("<####") && string.end_with?("####>")) 
    puts " [+] Padding found, removing...\n"
    string = string[5..string.length-5]
  end

  puts " [+] Using decode key: [ #{DECODE_KEY} ]\n"

  # Simple rotating xor
  output = ""
  offset = 0
  (0..string.length-1).each do |i|
    if(i % DECODE_KEY.length == 0)
      offset = 0
    end
    output << (string[i] ^ DECODE_KEY[offset])
    offset += 1
  end
  puts " [*] Decoded output : \n#{output}\n"

  puts " [+] Attempting to parse..."
  config = output.split(/#### /)
  puts " [*] C2 [variable : ha] = #{config[1]}"
  puts " [*] FTP Server [variable : fa] = #{config[2]}"
  puts " [*] FTP Username [variable : fm] = #{config[3]}"
  puts " [*] FTP Password [variable : fp] = #{config[4]}"
  puts " [*] AlarmServiceini-timehour [variable : th] = #{config[5]}"
  puts " [*] AlarmServiceini-timeminute [variable : tm] = #{config[6]}"
  puts " [*] Unused [variable : bol] = #{config[7]}"
  puts " [*] Unused telephone numbers [variable : num] = #{config[8]}"
end
