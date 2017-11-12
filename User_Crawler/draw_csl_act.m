function draw_csl_act()
    dataset_0 = csvread('./data/cross-site-linking/user_attr_0.csv', 1, 2);
    dataset_1 = csvread('./data/cross-site-linking/user_attr_1.csv', 1, 2);
    dataset_2 = csvread('./data/cross-site-linking/user_attr_2.csv', 1, 2);
    dataset_3 = csvread('./data/cross-site-linking/user_attr_3.csv', 1, 2);
    figure(1);
    avgs = [mean(dataset_0(:,10)), mean(dataset_1(:,10)), mean(dataset_2(:,10)), mean(dataset_3(:,10))];
    avgs = [avgs; mean(dataset_0(:,12)), mean(dataset_1(:,12)), mean(dataset_2(:,12)), mean(dataset_3(:,12))];
    avgs = [avgs; mean(dataset_0(:,11)), mean(dataset_1(:,11)), mean(dataset_2(:,11)), mean(dataset_3(:,11))];
    avgs = [avgs; mean(dataset_0(:,9)), mean(dataset_1(:,9)), mean(dataset_2(:,9)), mean(dataset_3(:,9))];
    X = {'Posts', 'Responses', 'Recommends', 'Highlights'};
    bar(avgs);
    colormap(copper);
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel(' ','FontSize',20);
    ylabel('Average Number','FontSize',20);
    legend('Neither', 'TW only', 'FB only', 'Both', 'Location', 'NorthWest');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/csl_act_bar.eps', '-depsc')
end