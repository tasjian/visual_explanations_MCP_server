#!/bin/bash

# Visual Explanation MCP Server Control Script
# Usage: ./server_control.sh [start|stop|restart|status|logs]

SERVER_NAME="Visual Explanation MCP Server"
PID_FILE=".server.pid"
LOG_FILE="server.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${BLUE}🎬 $SERVER_NAME Control 🎬${NC}"
    echo "=================================================="
}

check_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    fi
}

get_server_pid() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "$pid"
        else
            rm -f "$PID_FILE"
            echo ""
        fi
    else
        echo ""
    fi
}

start_server() {
    local pid=$(get_server_pid)
    
    if [ ! -z "$pid" ]; then
        echo -e "${YELLOW}⚠️  Server already running (PID: $pid)${NC}"
        echo -e "${BLUE}📺 Demo: http://localhost:8000/demo${NC}"
        return 0
    fi
    
    echo -e "${GREEN}🚀 Starting $SERVER_NAME...${NC}"
    check_venv
    
    source venv/bin/activate
    
    # Start server in background and capture PID
    nohup python run_server.py > "$LOG_FILE" 2>&1 &
    local server_pid=$!
    
    # Save PID to file
    echo "$server_pid" > "$PID_FILE"
    
    # Wait a moment and check if server started successfully
    sleep 3
    
    if ps -p "$server_pid" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Server started successfully (PID: $server_pid)${NC}"
        echo -e "${BLUE}📺 Demo: http://localhost:8000/demo${NC}"
        echo -e "${BLUE}📚 API docs: http://localhost:8000/docs${NC}"
        echo -e "${BLUE}📋 Logs: tail -f $LOG_FILE${NC}"
    else
        echo -e "${RED}❌ Failed to start server${NC}"
        echo -e "${YELLOW}📋 Check logs: cat $LOG_FILE${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_server() {
    local pid=$(get_server_pid)
    
    if [ -z "$pid" ]; then
        echo -e "${YELLOW}⚠️  Server not running${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}🛑 Stopping server (PID: $pid)...${NC}"
    
    # Try graceful shutdown first
    kill "$pid" 2>/dev/null
    
    # Wait up to 10 seconds for graceful shutdown
    local count=0
    while [ $count -lt 10 ] && ps -p "$pid" > /dev/null 2>&1; do
        sleep 1
        count=$((count + 1))
    done
    
    # If still running, force kill
    if ps -p "$pid" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚡ Force killing server...${NC}"
        kill -9 "$pid" 2>/dev/null
    fi
    
    rm -f "$PID_FILE"
    echo -e "${GREEN}✅ Server stopped${NC}"
}

restart_server() {
    echo -e "${BLUE}🔄 Restarting $SERVER_NAME...${NC}"
    stop_server
    sleep 2
    start_server
}

show_status() {
    local pid=$(get_server_pid)
    
    print_banner
    
    if [ ! -z "$pid" ]; then
        echo -e "${GREEN}✅ Server Status: RUNNING${NC}"
        echo -e "   PID: $pid"
        echo -e "   Started: $(ps -p "$pid" -o lstart= 2>/dev/null | xargs)"
        echo -e "   Memory: $(ps -p "$pid" -o rss= 2>/dev/null | xargs)KB"
        echo ""
        echo -e "${BLUE}🌐 URLs:${NC}"
        echo -e "   Demo: http://localhost:8000/demo"
        echo -e "   API:  http://localhost:8000/docs"
        echo ""
        
        # Test server responsiveness
        if command -v curl >/dev/null 2>&1; then
            if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q "200"; then
                echo -e "${GREEN}✅ Server responding to requests${NC}"
            else
                echo -e "${YELLOW}⚠️  Server running but not responding${NC}"
            fi
        fi
    else
        echo -e "${RED}❌ Server Status: STOPPED${NC}"
    fi
    
    # Show environment info
    echo ""
    echo -e "${BLUE}🔧 Environment:${NC}"
    if [ -f ".env" ]; then
        if grep -q "ANTHROPIC_API_KEY=" ".env" && [ -n "$(grep "ANTHROPIC_API_KEY=" ".env" | cut -d'=' -f2)" ]; then
            echo -e "   Anthropic API: ✅ Configured"
        else
            echo -e "   Anthropic API: ⚠️  Not configured"
        fi
    else
        echo -e "   .env file: ❌ Not found"
    fi
    
    if [ -d "venv" ]; then
        echo -e "   Virtual env: ✅ Present"
    else
        echo -e "   Virtual env: ❌ Missing"
    fi
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}📋 Server logs (last 20 lines):${NC}"
        echo "=================================="
        tail -20 "$LOG_FILE"
        echo "=================================="
        echo -e "${YELLOW}💡 For live logs: tail -f $LOG_FILE${NC}"
    else
        echo -e "${YELLOW}⚠️  No log file found${NC}"
    fi
}

show_help() {
    print_banner
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo -e "  ${GREEN}start${NC}    Start the server"
    echo -e "  ${YELLOW}stop${NC}     Stop the server"
    echo -e "  ${BLUE}restart${NC}  Restart the server"
    echo -e "  ${BLUE}status${NC}   Show server status"
    echo -e "  ${BLUE}logs${NC}     Show recent logs"
    echo -e "  ${BLUE}help${NC}     Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 start     # Start the server"
    echo "  $0 restart   # Restart the server"
    echo "  $0 status    # Check if running"
}

# Main script logic
case "$1" in
    start)
        print_banner
        start_server
        ;;
    stop)
        print_banner
        stop_server
        ;;
    restart)
        print_banner
        restart_server
        ;;
    status)
        show_status
        ;;
    logs)
        print_banner
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac