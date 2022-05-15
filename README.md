# cooperateAndBetray

社会中存在几种不同种类的人，多个人共同完成项目，每一次合作都有类似囚徒困境中的收益奖惩

## 人

- 能力值 $ability$：做事的能力，符合 $\mathrm{N}\left( \mu_{ability}, \sigma_{ability}^2\right)$，并且是正数
- 好感列表 $favorLst$：对所有人的好感列表，全部初始化为 $favorInit$
- 类别 $type$：对待项目的策略
  - $\mathrm{NICE}$：一直合作
  - $\mathrm{ORDINARY}$：始终选择合作，但如果对方背叛，就会投诉，如果被同一个人累计背叛 $n_{endurance}$ 次后，会将其加入黑名单 $blacklist$，拒绝与其共同承担项目，其中 $n_{endurance}$ 是容忍度。不同的人有不同的容忍度，符合 $\mathrm{N}\left( \mu_{endurance}, \sigma_{endurance}^2\right)$ 并取整
  - $\mathrm{BAD}$：刚开始选择合作，但是会在 $n_{cooperates}$ 次合作之后选择背叛试探别人底线，如果对方投诉，则将其加入白名单 $whitelist$，以后跟这个人共同承担项目时就会选择合作。不同的人有不同的 $n_{cooperates}$，符合 $\mathrm{N}\left( \mu_{cooperates}, \sigma_{cooperates}^2\right)$ 并取整
  - $\mathrm{EVIL}$：一直背叛


其中，$favorInit$ 、$\mu_{ability}$ 、$\sigma_{ability}$、$\mu_{endurance}$、$\sigma_{endurance}$、$\mu_{cooperates}$、$\sigma_{cooperates}$ 可由用户指定

## 项目人员确定

对于每个项目：

1. 项目的人数 $n_{group}$ 符合 $U\left( {\underline{n_{group}}},{\overline{n_{group}}}\right)$
2. 所有类别为 $\mathrm{NICE}$ 或 $\mathrm{ORDINARY}$ 的人根据对其他每个人的好感，使用轮盘赌选择法，分别投出1票
3. 根据投票数，使用轮盘赌选择法，不断选择项目人员 $x$，直到人数达到 $n_{group}$。注意如果存在另一个组员 $y \in x.blacklist$ 中，则 $x$ 拒绝加入项目

其中，$\underline{n_{group}}$ 和 $\overline{n_{group}}$ 可由用户指定

## 收益与损失的计算

一个项目 $group$ 可划分为 $cluster1$ 和 $cluster2$

- 如果 $cluster1$ 和 $cluster2$ 相互背叛，则 $group$ 中每个人损失 $loss_{betray}$ 
- 如果 $cluster1$ 和 $cluster2$ 相互合作，则 $group$ 中每个人收益 $profit_{cooperate}$。对一个人 $x$ ，定义 $friends_{x}$ 为 $x.favorLst$ 最高的 $n_{friends}$ 个人，令 $S=\left\{ friends_{x} \mid x\in group\right\} \cup \left\{ group\right\}$，$S$ 中每个人对$group$ 中每个人 $y$ 的好感提升 $\frac{y.ability}{2}$
- 如果 $cluster1$ 选择与 $cluster2$ 合作，但 $cluster2$ 背叛了 $cluster1$
  - 首先，$cluster1$ 中每人损失 $loss_{cooperate}$，$cluster2$ 中每人收益 $profit_{betray}$
  - 随后，$cluster1$ 中进行投诉的人每人损失 $loss_{askForComplaint}$，$cluster2$ 中每个人需要赔偿 $loss_{complaint} \times n_{complaint}$，其中 $n_{complaint}$ 是投诉人数，赔偿将平均分为 $cluster1$ 中的每个人
  - 最后，对 $S=\left\{ friends_{x} \mid x\in cluster1\right\} \cup \left\{ cluster1\right\}$ ，令 $S$ 的每个人对 $cluster1$ 中的每个人 $y$ 的好感提升 $\frac{y.ability}{2}$，对 $cluster2$ 中每个人的好感降低 $\frac{\sum_{x\in{cluster1}}x.ability}{\left| {cluster1}\right|}$ 

其中 $loss_{askForComplaint}$、$loss_{complaint}$、 $n_{friends}$、 $loss_{betray}$、$profit_{cooperate}$、$loss_{cooperate}$ 和 $profit_{betray} $ 均可由用户指定

