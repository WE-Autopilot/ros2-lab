#ifndef AP1_MPC_CONTROLLER_HPP
#define AP1_MPC_CONTROLLER_HPP

#include <cmath>
#include <limits>
#include <vector>

#include "ap1/control/icontroller.hpp"
#include "vectors.hpp"

namespace ap1::control
{
class MPCController : public IController
{
  public:
    explicit MPCController(float dt = 1.0f / 60.0f)
        : dt_(dt)
    {
    }

    // Tuning setters (optional)
    void set_horizon(int N) { horizon_ = (N < 1 ? 1 : N); }
    void set_accel_limits(float amax_x, float amax_y)
    {
        amax_x_ = std::fabs(amax_x);
        amax_y_ = std::fabs(amax_y);
    }

    void set_weights(float w_pos, float w_speed, float w_u)
    {
        w_pos_ = w_pos;
        w_speed_ = w_speed;
        w_u_ = w_u;
    }

    vec3f compute_acceleration(const vec3f& vel,
                               const vec2f& target_pos,
                               const float target_speed) override
    {
        // Candidate accelerations. Keep small and robust.
        // You can expand this grid later if needed.
        std::vector<float> ax_candidates = {
            -amax_x_, -0.5f * amax_x_, 0.0f, 0.5f * amax_x_, amax_x_
        };
        std::vector<float> ay_candidates = {
            -amax_y_, -0.5f * amax_y_, 0.0f, 0.5f * amax_y_, amax_y_
        };

        float best_cost = std::numeric_limits<float>::infinity();
        vec3f best_a(0.0f, 0.0f, 0.0f);

        // Initial state in car frame
        vec2f p0(0.0f, 0.0f);
        vec2f v0(vel.x, vel.y);

        for (float ax : ax_candidates)
        {
            for (float ay : ay_candidates)
            {
                float cost = rollout_cost(p0, v0, target_pos, target_speed, ax, ay);

                if (cost < best_cost)
                {
                    best_cost = cost;
                    best_a = vec3f(ax, ay, 0.0f);
                }
            }
        }

        return best_a;
    }

  private:
    float dt_;
    int horizon_ = 12;          // 12 steps at 60Hz ≈ 0.2s horizon
    float amax_x_ = 2.0f;       // m/s^2 longitudinal
    float amax_y_ = 2.0f;       // m/s^2 lateral

    // Cost weights
    float w_pos_ = 2.0f;
    float w_speed_ = 1.0f;
    float w_u_ = 0.05f;

    static float sq(float x) { return x * x; }

    float rollout_cost(vec2f p,
                       vec2f v,
                       const vec2f& target_pos,
                       float target_speed,
                       float ax,
                       float ay) const
    {
        float cost = 0.0f;

        // simulate assuming constant acceleration over horizon
        for (int k = 0; k < horizon_; k++)
        {
            // advance position
            p.x += v.x * dt_;
            p.y += v.y * dt_;

            // advance velocity
            v.x += ax * dt_;
            v.y += ay * dt_;

            // optional: prevent reversing (your comment says forward only "atp")
            if (v.x < 0.0f)
                v.x = 0.0f;

            // position error to target
            const float ex = (target_pos.x - p.x);
            const float ey = (target_pos.y - p.y);

            // speed error (use forward speed)
            const float es = (target_speed - v.x);

            // stage cost
            cost += w_pos_ * (sq(ex) + sq(ey));
            cost += w_speed_ * sq(es);
            cost += w_u_ * (sq(ax) + sq(ay));
        }

        return cost;
    }
};
} // namespace ap1::control

#endif // AP1_MPC_CONTROLLER_HPP
