library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fsm_controller is
  Port (
    clk, reset     : in  std_logic;
    key_ready      : in  std_logic;
    keycode        : in  std_logic_vector(7 downto 0);
    load_A, load_B : out std_logic;
    load_op        : out std_logic;
    load_result    : out std_logic;
    compute        : out std_logic;
    disp_update    : out std_logic
  );
end fsm_controller;

architecture Behavioral of fsm_controller is
  type state_type is (
    IDLE, WAIT_OP1, LOAD_OP1, WAIT_OP2, LOAD_OP2,
    WAIT_OPR, LOAD_OPR, WAIT_EQ, DO_COMPUTE, DISPLAY_RESULT
  );
  signal state : state_type := IDLE;
begin
  process(clk, reset)
  begin
    if reset = '1' then
      state <= IDLE;
    elsif rising_edge(clk) then
      load_A      <= '0';
      load_B      <= '0';
      load_op     <= '0';
      compute     <= '0';
      load_result <= '0';
      disp_update <= '0';

      case state is
        when IDLE =>
          if key_ready = '1' then state <= WAIT_OP1; end if;

        when WAIT_OP1 =>
          if key_ready = '1' then state <= LOAD_OP1; end if;

        when LOAD_OP1 =>
          load_A  <= '1';
          state   <= WAIT_OP2;

        when WAIT_OP2 =>
          if key_ready = '1' then state <= LOAD_OP2; end if;

        when LOAD_OP2 =>
          load_B  <= '1';
          state   <= WAIT_OPR;

        when WAIT_OPR =>
          if key_ready = '1' then state <= LOAD_OPR; end if;

        when LOAD_OPR =>
          load_op <= '1';
          state   <= WAIT_EQ;

        when WAIT_EQ =>
          if key_ready = '1' and keycode = x"5A" then
            state <= DO_COMPUTE;
          end if;

        when DO_COMPUTE =>
          compute     <= '1';
          load_result <= '1';
          state       <= DISPLAY_RESULT;

        when DISPLAY_RESULT =>
          disp_update <= '1';
          state       <= IDLE;

        when others =>
          state <= IDLE;
      end case;
    end if;
  end process;
end Behavioral;
