function draw_impact_csl()
    dataset_0 = csvread('./data/cross-site-linking/user_attr_0.csv', 1, 2);
    dataset_1 = csvread('./data/cross-site-linking/user_attr_1.csv', 1, 2);
    dataset_2 = csvread('./data/cross-site-linking/user_attr_2.csv', 1, 2);
    dataset_3 = csvread('./data/cross-site-linking/user_attr_3.csv', 1, 2);
    high_impact = [sum(dataset_0(:,6)>9.1746e-06), sum(dataset_1(:,6)>9.1746e-06), sum(dataset_2(:,6)>9.1746e-06), sum(dataset_3(:,6)>9.1746e-06)];
    less_impact = [sum(dataset_0(:,6)<=9.1746e-06), sum(dataset_1(:,6)<=9.1746e-06), sum(dataset_2(:,6)<=9.1746e-06), sum(dataset_3(:,6)<=9.1746e-06)];
    Y = [high_impact/sum(high_impact); less_impact/sum(less_impact)];
    X = {'High Influential', 'Less Influential'};
    bar(Y, 0.8, 'stacked');
    colormap(copper);
    xlim([0.5 2.5]); 
    ylim([0 1]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    ax = gca;
    ax.XAxis.FontSize = 18;
    xlabel(' ','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend('Neither', 'TW only', 'FB only', 'Both', 'Location', 'EastOutside');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/impact_csl.eps', '-depsc');
    disp(high_impact);
    disp(less_impact);
    disp(Y);
end