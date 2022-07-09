

nx75_protocol = Proto("nx75",  "NX75 Configuration Protocol")

local startbyte = ProtoField.uint8("nx75.startbyte", "Start byte", base.HEX)
local cmdbyte1 = ProtoField.uint8("nx75.cmdbyte1", "cmdbyte1", base.HEX)
local idkbytes1 = ProtoField.bytes("nx75.idkbytes1", "idkbytes1")
local cmdbyte2 = ProtoField.uint8("nx75.cmdbyte2", "cmdbyte2", base.HEX)
local argword1 = ProtoField.uint32("nx75.argword1", "argword1", base.HEX)
local restbytes = ProtoField.bytes("nx75.restbytes", "Rest of bytes")

nx75_protocol.fields = {startbyte, cmdbyte1, idkbytes1, cmdbyte2, argword1, restbytes}


-- max_gap.lua
-- create a gap.max field containing the maximum gap between two packets between two ip nodes

-- we create a "protocol" for our tree
local max_gap_p = Proto("gap","Gap in IP conversations")

-- we create our fields
local max_gap_field = ProtoField.float("gap.max")

data_fragment_f = Field.new("usb.data_fragment")


-- we add our fields to the protocol
max_gap_p.fields = { max_gap_field }

-- then we register max_gap_p as a postdissector
register_postdissector(max_gap_p)

local gaps = {} -- the maximum gap sofar between two nodes  
local last = {} -- the last time a packet was seen between two nodes

-- a debug logging function (adds into dissector proto tree)
local enable_logging = true   -- set this to true to enable it!!
local function initLog(tree, proto)
    if not enable_logging then
        -- if logging is disabled, we return a dummy function
        return function() return end
    end
    local log_tree = tree:add(proto, nil, "Debug Log")
    log_tree:set_generated()
    -- return a function that when called will add a new child with the given text
    return function(str) log_tree:add(proto):set_text(str) end
end

-- let's do it!
function max_gap_p.dissector(tvb,pinfo,tree)

    local addr_lo = pinfo.net_src
    local addr_hi = pinfo.net_dst

    if addr_lo > addr_hi then
        addr_hi,addr_lo = addr_lo,addr_hi
    end

    local conv_key =  tostring(addr_lo) .. " " .. tostring(addr_hi)
    local this_gap = 0
    local max_gap = 0

    -- initialize logging, getting the logging function to use later
    local log = initLog(tree,max_gap_p)
    
    log("Key:" .. tostring(conv_key))
    log("Visited: " .. tostring(pinfo.visited))
    
    local data_fragment = data_fragment_f()

    if data_fragment then
        log("data_fragment: " .. tostring(data_fragment))
        
        local nx75tree = tree:add(nx75_protocol, tvb(data_fragment.offset, data_fragment.len), "NX75 packet")

        
        nx75tree:add(startbyte,     tvb(data_fragment.offset +  0, 1))
        nx75tree:add(cmdbyte1,      tvb(data_fragment.offset +  1, 1))
        nx75tree:add(idkbytes1,     tvb(data_fragment.offset +  2, 7))
        nx75tree:add(cmdbyte2,      tvb(data_fragment.offset +  9, 1))
        nx75tree:add(argword1,      tvb(data_fragment.offset + 10, 4))
        nx75tree:add(restbytes,     tvb(data_fragment.offset + 14, data_fragment.len - 14))
    end

    
    if not pinfo.visited then
        local now = pinfo.rel_ts

        log("Now: "..now)
        
        if last[conv_key] then 
            this_gap = now - last[conv_key]

            log("A subsequent Packet, Gap: "..this_gap)
            
            if gaps[conv_key] then
                max_gap = gaps[conv_key]
                log("Got Old Max Gap: " .. max_gap)
            end
            
            if max_gap < this_gap then
                log("New Gap is Bigger")
                gaps[conv_key] = this_gap
                max_gap = this_gap
            end
        else
            log("First Packet, no gap!")
        end 

        last[conv_key] = now

    else
       max_gap = gaps[conv_key]
    end
    
    if max_gap then
        tree:add(max_gap_field,max_gap):set_generated()
    end

end