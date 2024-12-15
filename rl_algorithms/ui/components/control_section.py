# ui/components/control_section.py
import pygame
from core.algorithms.policy_iteration import PolicyIteration
from core.algorithms.value_iteration import ValueIteration

class ControlSection:
    def __init__(self, viz, left, top, width, font, colors):
        self.viz = viz
        self.left = left
        self.top = top
        self.width = width
        self.font = font
        self.BLACK = colors['BLACK']
        self.WHITE = colors['WHITE']

        self.evaluation_steps = 0
        self.iteration_steps = 0
        self.is_eval_converged = False
        self.is_policy_converged = False

        self.cont_sec_title = {'text': 'Algorithm Control', 'rect': pygame.Rect(
            left+20, top+20, width, 40)}

        self.eval_step_counter = {'text': f'Evaluation Steps: {self.evaluation_steps}', 'rect': pygame.Rect(
            left+20, top+70, width, 40)}
        self.iter_step_counter = {'text': f'Iteration Steps: {self.iteration_steps}', 'rect': pygame.Rect(
            left+20, top+170, width, 40)}

        # For Policy Iteration
        self.algo_control_buttons = [
            {'text': 'Policy Evaluation', 'rect': pygame.Rect(left+20, top+120, width, 40), 'visible': False},
            {'text': 'Policy Improvement', 'rect': pygame.Rect(left+20, top+220, width, 40), 'visible': False},
            {'text': 'Reset Algorithm', 'rect': pygame.Rect(left+20, top+270, width, 40), 'visible': False},

            # For Value Iteration
            {'text': 'Iterate one step', 'rect': pygame.Rect(left+20, top+220, width, 40), 'visible': False},

            # For Model-Free algorithms
            {'text': 'Generate Experience', 'rect': pygame.Rect(left+20, top+320, width, 40), 'visible': False},
        ]

        # Agent control
        self.agent_sec_title = {'text': 'Agent Control', 'rect': pygame.Rect(
            left+20, top+370, width, 40)}
        self.agent_control_buttons = [
            {'text': 'Move Agent', 'rect': pygame.Rect(left+20, top+420, width, 40), 'visible': True},
            {'text': 'Reset Agent', 'rect': pygame.Rect(left+20, top+470, width, 40), 'visible': True},
        ]

        self.selected_action = None

    def draw(self, screen, window_size, current_alg):
        # Title
        pygame.draw.rect(screen, self.WHITE, self.cont_sec_title['rect'])
        text = self.font.render(self.cont_sec_title['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.cont_sec_title['rect'].center)
        screen.blit(text, text_rect)

        # Draw according to algorithm type
        if isinstance(current_alg, PolicyIteration):
            self._draw_policy_iteration_controls(screen)
        elif isinstance(current_alg, ValueIteration):
            self._draw_value_iteration_controls(screen)
        # else: no controls visible if no algorithm chosen

        # Agent Control Title
        pygame.draw.rect(screen, self.WHITE, self.agent_sec_title['rect'])
        agent_text = self.font.render(self.agent_sec_title['text'], True, self.BLACK)
        agent_text_rect = agent_text.get_rect(center=self.agent_sec_title['rect'].center)
        screen.blit(agent_text, agent_text_rect)

        for button in self.agent_control_buttons:
            pygame.draw.rect(screen, self.WHITE, button['rect'])
            pygame.draw.rect(screen, self.BLACK, button['rect'], 1)
            t = self.font.render(button['text'], True, self.BLACK)
            t_rect = t.get_rect(center=button['rect'].center)
            screen.blit(t, t_rect)

    def _draw_policy_iteration_controls(self, screen):
        # Update counters
        self.eval_step_counter['text'] = f'Evaluation Steps: {self.evaluation_steps}'
        text = self.font.render(self.eval_step_counter['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.eval_step_counter['rect'].center)
        screen.blit(text, text_rect)

        self.iter_step_counter['text'] = f'Iteration Steps: {self.iteration_steps}'
        text = self.font.render(self.iter_step_counter['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.iter_step_counter['rect'].center)
        screen.blit(text, text_rect)

        for i, button in enumerate(self.algo_control_buttons):
            if i > 2:
                button['visible'] = False
            else:
                button['visible'] = True
                pygame.draw.rect(screen, self.WHITE, button['rect'])
                pygame.draw.rect(screen, self.BLACK, button['rect'], 1)
                t = self.font.render(button['text'], True, self.BLACK)
                t_rect = t.get_rect(center=button['rect'].center)
                screen.blit(t, t_rect)

    def _draw_value_iteration_controls(self, screen):
        self.iter_step_counter['text'] = f'Iteration Steps: {self.iteration_steps}'
        text = self.font.render(self.iter_step_counter['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.iter_step_counter['rect'].center)
        screen.blit(text, text_rect)

        for i, button in enumerate(self.algo_control_buttons):
            if i < 2 or i > 3:
                button['visible'] = False
            else:
                button['visible'] = True
                pygame.draw.rect(screen, self.WHITE, button['rect'])
                pygame.draw.rect(screen, self.BLACK, button['rect'], 1)
                t = self.font.render(button['text'], True, self.BLACK)
                t_rect = t.get_rect(center=button['rect'].center)
                screen.blit(t, t_rect)

    # ---[새로 추가할 메서드들]---

    def update_algorithm(self, algorithm):
        """
        UIUpdateObserver에서 algorithm_changed 이벤트가 발생했을 때 호출됨.
        필요한 초기화나 상태 설정을 여기서 진행.
        """
        # 알고리즘 변경 시, 평가/개선 단계 및 수 convergence 상태를 초기화
        self.evaluation_steps = 0
        self.iteration_steps = 0
        self.is_eval_converged = False
        self.is_policy_converged = False

    def update_evaluation(self, eval_data):
        """
        policy_evaluation 이벤트가 발생했을 때 옵저버에서 호출됨.
        eval_data 예: {'steps': int, 'delta': float, 'converged': bool}
        """
        self.evaluation_steps = eval_data.get('steps', self.evaluation_steps)
        # delta나 converged 상태를 UI에 반영할 수도 있음.

    def handle_click(self, pos, current_alg):
        # Algo control buttons
        for i, button in enumerate(self.algo_control_buttons):
            if button['visible'] and button['rect'].collidepoint(pos):
                if current_alg is None:
                    self.viz.show_toast("Please select an algorithm first!")
                else:
                    if button['text'] == 'Policy Evaluation':
                        self.policy_evaluation(current_alg)
                    elif button['text'] == 'Policy Improvement':
                        self.policy_improvement(current_alg)
                    elif button['text'] == 'Reset Algorithm':
                        self.reset_algorithm(current_alg)
                    elif button['text'] == 'Iterate one step':
                        self.algo_step(current_alg)

        # Agent control buttons
        for i, button in enumerate(self.agent_control_buttons):
            if button['rect'].collidepoint(pos):
                if current_alg is None:
                    self.viz.show_toast("Please select an algorithm first!")
                else:
                    if button['text'] == 'Move Agent':
                        self.move_agent(current_alg)
                    elif button['text'] == 'Reset Agent':
                        self.reset_agent(current_alg)

    def update_algorithm(self, algorithm):
        """
        UIUpdateObserver에서 algorithm_changed 이벤트가 발생했을 때 호출됨.
        필요한 초기화나 상태 설정을 여기서 진행.
        """
        # 알고리즘 변경 시, 평가/개선 단계 및 수 convergence 상태를 초기화
        self.evaluation_steps = 0
        self.iteration_steps = 0
        self.is_eval_converged = False
        self.is_policy_converged = False

    def update_evaluation(self, eval_data):
        """
        policy_evaluation 이벤트가 발생했을 때 옵저버에서 호출됨.
        eval_data 예: {'steps': int, 'delta': float, 'converged': bool}
        """
        self.evaluation_steps = eval_data.get('steps', self.evaluation_steps)
        # delta나 converged 상태를 UI에 반영할 수도 있음.

    def policy_evaluation(self, current_alg):
        if self.is_eval_converged:
            self.viz.show_toast("Policy evaluation already converged!")
        else:
            delta = current_alg.policy_evaluation_step()
            self.evaluation_steps += 1
            self.is_policy_converged = False
            self.viz.notify_observers('policy_evaluation', {
                'steps': self.evaluation_steps,
                'delta': delta,
                'converged': delta < 1e-6
            })

            if delta < 1e-6:
                self.viz.show_toast("Policy evaluation converged!")
                self.is_eval_converged = True

    def policy_improvement(self, current_alg):
        if self.evaluation_steps == 0:
            self.viz.show_toast("Please perform policy evaluation first!")
        elif self.is_policy_converged:
            self.viz.show_toast("Policy improvement already converged!")
        else:
            is_converged = current_alg.policy_improvement_step()
            self.evaluation_steps = 0
            self.is_eval_converged = False
            if is_converged:
                self.viz.show_toast("Policy improvement converged!")
                self.is_policy_converged = True
            self.iteration_steps += 1

    def reset_algorithm(self, current_alg):
        current_alg.reset()
        self.evaluation_steps = 0
        self.iteration_steps = 0
        self.is_eval_converged = False
        self.is_policy_converged = False

    def algo_step(self, current_alg):
        if self.is_policy_converged:
            self.viz.show_toast("Policy improvement already converged!")
        else:
            is_converged = current_alg.step()
            self.iteration_steps += 1
            if is_converged:
                self.viz.show_toast("Algorithm converged!")
                self.is_policy_converged = True

    def move_agent(self, current_alg):
        if self.viz.env.is_terminated():
            self.viz.show_toast("Agent already reached terminal state!")
        else:
            self.selected_action = current_alg.select_action(self.viz.env.agent_state)
            done = current_alg.move_agent(self.selected_action)
            self.viz.notify_observers('agent_moved', {
                'action': self.selected_action,
                'state': self.viz.env.agent_state,
                'done': done
            })
            if done:
                self.viz.show_toast("Agent reached terminal state!")

    def reset_agent(self, current_alg):
        current_alg.reset_agent()